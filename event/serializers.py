from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from event.models import Event


class EventSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = ['uuid', 'title', 'content', 'date', 'flag']
        extra_kwargs = {
            "uuid": {'required': False},
            "title": {'required': True},
            "date": {'required': True},
        }
        lookup_field = 'uuid'

    def to_representation(self, obj):
        data = super(EventSerializer, self).to_representation(obj)
        data['date'] = {
            'year': obj.date.year,
            'month': obj.date.month,
            'day': obj.date.day,
            'hour': obj.date.hour,
            'minute': obj.date.minute,
        }
        return data

    def create(self, validated_data):
        request = self.context['request']
        return Event.objects.create(user=request.user, **validated_data)
