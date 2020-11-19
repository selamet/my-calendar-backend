from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/user/', include('user.api.urls', namespace='user')),
    path('api/event/', include('event.urls', namespace='event')),

]
