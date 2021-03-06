from django.core.exceptions import ValidationError
from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
import datetime

from event.models import Event
from event.serializers import EventSerializer
from event.permissions import IsOwner


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = (IsAuthenticated, IsOwner)
    lookup_field = 'uuid'

    def list(self, request, *args, **kwargs):
        uuid = kwargs.get('uuid', {})
        from_date = request.GET.get('from', '')
        to_date = request.GET.get('to', '')
        date_range = [from_date, to_date]
        try:
            queryset = Event.objects.filter(user=request.user, date__range=date_range)
        except ValidationError as err:
            return Response(err, 400)

        if uuid:
            queryset = queryset.filter(uuid=uuid)

        serializer = EventSerializer(queryset, many=True)

        return Response(serializer.data)

    def perform_destroy(self, instance):
        if self.request.user != instance.user:
            from django.core.exceptions import PermissionDenied
            raise PermissionDenied()
        instance.delete()
