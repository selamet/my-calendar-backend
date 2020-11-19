from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from event.models import Event
from event.serializers import EventSerializer


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = 'uuid'

    def list(self, request, *args, **kwargs):
        uuid = kwargs.get('uuid', {})
        queryset = Event.objects.filter(user=request.user)
        if uuid:
            queryset = queryset.filter(uuid=uuid)
        serializer = EventSerializer(queryset, many=True)
        return Response(serializer.data)
