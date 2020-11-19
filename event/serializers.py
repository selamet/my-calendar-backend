from rest_framework import serializers

from event.models import Event


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['uuid', 'user', 'title', 'content', 'date', 'flag']
        extra_kwargs = {
            "uuid": {'required': False},
            "user": {'required': False},
            "title": {'required': True},
            "date": {'required': True},
        }
        lookup_field = 'uuid'

    def create(self, validated_data):
        request = self.context['request']
        return Event.objects.create(user=request.user, **validated_data)
