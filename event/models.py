from django.db import models

# Create your models here.
from libs.models import BaseModel
from django.contrib.auth.models import User
import uuid

FLAG_CHOICES = [
    ('4', 'Red'),
    ('3', 'Blue'),
    ('2', 'Green'),
    ('1', 'Yellow'),
    ('0', 'None')
]


class Event(BaseModel):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='user')
    title = models.CharField(max_length=50, verbose_name="title")
    content = models.CharField(max_length=50, verbose_name="content", blank=True)
    date = models.DateTimeField()
    flag = models.CharField(max_length=1, choices=FLAG_CHOICES, default='0')

    def __str__(self):
        return self.title
