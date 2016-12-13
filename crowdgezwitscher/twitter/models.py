from __future__ import unicode_literals

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils.encoding import python_2_unicode_compatible
from django.db.models.signals import post_save
from django.db import IntegrityError
from django.dispatch import receiver

from datetime import datetime

from crowdgezwitscher.log import logger
from TwitterAPI import TwitterAPI, TwitterConnectionError

@python_2_unicode_compatible
class TwitterAccount(models.Model):
    name = models.CharField(max_length=15, unique=True)
    account_id = models.CharField(max_length=15, unique=True)
    last_known_tweet_id = models.CharField(max_length=20)

    def __repr__(self):
        return '<TwitterAccount %s>' % self.name

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('twitter:detail', kwargs={'pk': self.pk})

    def clean(self):
        twitter = TwitterAPI(settings.TWITTER_CONSUMER_KEY,
                        settings.TWITTER_CONSUMER_SECRET,
                        auth_type='oAuth2')
        try:
            user = twitter.request('users/show', {'screen_name': self.name}).json()
        except TwitterConnectionError:
            logger.warning("Could not connect to Twitter.")
            raise ValidationError("Could not connect to Twitter to retrieve user_id.")
        if 'id_str' in user:
            self.account_id = user['id_str']
        else:
            logger.warning("Could not find user with provided name.")
            raise ValidationError("Could not find user with provided name.")

    def _fetch_tweets_from_api(self, twitter, max_id=None):
        request_parameters = {
            'count': 200,
            'user_id': self.account_id,
            'trim_user': True,
            'exclude_replies': True,
            'contributor_details': False,
        }

        # max_id is optional and not known for first request
        if max_id:
            request_parameters['max_id'] = max_id

        return twitter.request('statuses/user_timeline',request_parameters).json()

    def fetch_initial_tweets(self):
        new_tweets = []
        tweet_hashtag_mappings = {}
        twitter = TwitterAPI(settings.TWITTER_CONSUMER_KEY,
                             settings.TWITTER_CONSUMER_SECRET,
                             auth_type='oAuth2')

        try:
            tweets_from_api = self._fetch_tweets_from_api(twitter)
            while tweets_from_api:
                for tweet_from_api in tweets_from_api:
                    tweet = Tweet(tweet_id=tweet_from_api['id_str'], content=tweet_from_api['text'], account=self)
                    print tweet_from_api['']
                    new_tweets.append(tweet)
                    hashtags = []
                    for hashtag_from_api in tweet_from_api['entities']['hashtags']:
                        hashtag_text = hashtag_from_api['text']
                        hashtag, _ = Hashtag.objects.get_or_create(hashtag_text=hashtag_text)
                        hashtags.append(hashtag)
                    tweet_hashtag_mappings[tweet.tweet_id] = hashtags
                tweets_from_api = self._fetch_tweets_from_api(twitter, int(new_tweets[-1].tweet_id) - 1)
        except TwitterConnectionError:
            logger.warning("Could not connect to Twitter.")

        Tweet.objects.bulk_create(new_tweets)
        for tweet in self.tweet_set.all():
            tweet.hashtags.add(*(tweet_hashtag_mappings.get(tweet.tweet_id, [])))
            tweet.save()


@python_2_unicode_compatible
class Hashtag(models.Model):
    hashtag_text = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.hashtag_text


@python_2_unicode_compatible
class Tweet(models.Model):
    tweet_id = models.CharField(max_length=20, unique=True)
    content = models.CharField(max_length=250)
    account = models.ForeignKey(TwitterAccount, on_delete=models.CASCADE)
    hashtags = models.ManyToManyField(Hashtag)
    created_at = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return "%s - %s" % (self.account, self.content)