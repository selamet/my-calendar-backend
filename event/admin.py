from django.contrib import admin
from event.models import Event


# Register your models here.

class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'uuid', 'user')
    list_filter = ['user']


admin.site.register(Event, EventAdmin)
