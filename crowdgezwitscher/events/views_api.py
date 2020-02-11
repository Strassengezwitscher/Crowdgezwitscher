from datetime import datetime, timedelta

from rest_framework import generics, status
from rest_framework.decorators import authentication_classes, api_view, parser_classes
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView

from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db.models.functions import TruncYear

from base.models import MapObjectFilterBackend
from crowdgezwitscher.log import logger
from crowdgezwitscher.auth import CsrfExemptSessionAuthentication
from events.filters import DateFilterBackend
from events.models import Event
from events.serializers import EventSerializer, EventSerializerShortened, EventSerializerCreate
from twitter.models import Tweet


class EventAPIList(generics.ListAPIView):
    queryset = Event.objects.filter(active=True)
    serializer_class = EventSerializerShortened
    filter_backends = (
        DateFilterBackend,
        MapObjectFilterBackend,
    )


class EventAPIDetail(generics.RetrieveAPIView):
    queryset = Event.objects.filter(active=True)
    serializer_class = EventSerializer


class EventAPIGetTweets(APIView):
    def get(self, request, pk, format=None):
        """Get tweets for Event with primary key pk.

        Searches for saved tweets matching the Event's registered hashtags, accounts and dates.
        The dates form an open interval.
        """
        event = get_object_or_404(Event, pk=pk, active=True)
        if not event.coverage:
            return Response([])

        event_hashtag_ids = [hashtag.id for hashtag in event.hashtags.all()]

        try:
            since_id = int(request.query_params.get('since_id', 0))
        except ValueError:
            raise ValidationError({'message': "Please provide since_id as int."})
        if since_id < 0:
            raise ValidationError({'message': "since_id must be ≥ 0."})

        # Convert event coverage dates to datetimes as they will be compared to Tweets' creation datetimes.
        # The time part will be set to 00:00:00.
        # tweets_till would therefore be the earliest possible datetime for coverage_end. As we want to includes dates
        # from that date, we add another day to tweets_till.
        tweets_from = timezone.make_aware(datetime(
            event.coverage_start.year,
            event.coverage_start.month,
            event.coverage_start.day
        ))
        tweets_till = timezone.make_aware(datetime(
            event.coverage_end.year,
            event.coverage_end.month,
            event.coverage_end.day
        )) + timedelta(days=1)

        # It would be possible also use the __date field lookup of created_at before using __range.
        # This would allow using coverage_start and coverage_end, so no need for tweets_from and tweets_till.
        # However, this would nearly double the processing time.
        # The tweets are sorted in descending order to return the newest tweets first.
        tweets = Tweet.objects.filter(
            account__in=event.twitter_accounts.all(),
            created_at__range=(tweets_from, tweets_till),
            tweet_id__gt=since_id,
        ).order_by('-tweet_id')

        # If the event specifies hashtags, each tweet needs to include at least one of them.
        # Otherwise, there are no restrictions on tweets' hashtags.
        if event_hashtag_ids:
            tweets = tweets.filter(hashtags__in=event_hashtag_ids)

        # If a tweet and the event have multiple hashtags in common, the tweet is included multiple times.
        # We therefore need to call distinct().
        return Response([str(tweet.tweet_id) for tweet in tweets.distinct()])

class EventAPIYears(APIView):
    def get(self, request):
        years_queryset = Event.objects.all().annotate(year=TruncYear('date'))\
                                            .values('year')\
                                            .distinct()\
                                            .order_by('year')
        years_list = [entry['year'].year for entry in years_queryset]
        return Response(years_list)


@api_view(['POST'])
@authentication_classes((CsrfExemptSessionAuthentication,))
@parser_classes((JSONParser,))
def send_form(request):
    serializer = EventSerializerCreate(data=request.data)
    if not serializer.is_valid():
        return Response({'status': 'error', 'message': 'Fehler beim Speichern der Informationen. \n' + '\n'.join([serializer.errors[msg][0] for msg in serializer.errors])},
                        status=status.HTTP_400_BAD_REQUEST)
    try:
        serializer.save()
    except Exception as e:
        return Response({'status': 'error', 'message': 'Fehler beim Speichern der Informationen.'},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response({'status': 'success'})
