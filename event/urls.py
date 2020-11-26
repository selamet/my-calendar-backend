from django.urls import path

from event.views import EventViewSet

from rest_framework import routers

app_name = 'event'

router = routers.DefaultRouter()
router.register(r'', EventViewSet, )

urlpatterns = [
    path('<uuid>', EventViewSet.as_view({'patch': 'partial_update', 'get': 'list', 'delete': 'destroy'})),
]

urlpatterns += router.urls
