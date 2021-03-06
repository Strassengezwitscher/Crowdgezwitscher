from rest_framework import serializers

from facebook.models import FacebookPage


class FacebookPageSerializer(serializers.ModelSerializer):
    facebookId = serializers.CharField(source='facebook_id')

    class Meta:
        model = FacebookPage
        fields = (
            'id',
            'facebookId',
            'location',
            'name',
            'notes',
        )


class FacebookPageSerializerShortened(serializers.ModelSerializer):
    # TODO unify with EventSerializerShortened, issue: Cannot use ModelSerializer with Abstract Models.
    locationLong = serializers.DecimalField(
        source='location_long',
        max_digits=9,
        decimal_places=6,
        coerce_to_string=False,
    )
    locationLat = serializers.DecimalField(
        source='location_lat',
        max_digits=9,
        decimal_places=6,
        coerce_to_string=False,
    )

    class Meta:
        model = FacebookPage
        fields = (
            'id',
            'locationLat',
            'locationLong',
            'name',
        )

class FacebookPageSerializerCreate(serializers.ModelSerializer):
    locationLong = serializers.DecimalField(source='location_long',
                                            max_digits=17,
                                            decimal_places=15,
                                            )
    locationLat = serializers.DecimalField(source='location_lat',
                                            max_digits=17,
                                            decimal_places=15,
                                            )
    facebookId = serializers.CharField(source='facebook_id')

    class Meta:
        model = FacebookPage
        fields = ('id', 'name', 'location', 'notes', 'locationLong', 'locationLat', 'facebookId')

    def create(self, validated_data):
        return FacebookPage.objects.create(**validated_data)
