from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
import datetime

from event.models import Event
from event.serializers import EventSerializer


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = 'uuid'

    def list(self, request, *args, **kwargs):
        uuid = kwargs.get('uuid', {})
        from_date = request.GET.get('from', '')
        to_date = request.GET.get('to', '')
        if not (from_date or to_date):
            now = datetime.datetime.now()
            from_date = '{}-{}-{}'.format(now.year, now.month, 1)
            to_date = '{}-{}-{}'.format(now.year, now.month + 1, 1)
        date_range = [from_date, to_date]
        queryset = Event.objects.filter(user=request.user, date__range=date_range)

        if uuid:
            queryset = queryset.filter(uuid=uuid)

        serializer = EventSerializer(queryset, many=True)

        return Response(serializer.data)
