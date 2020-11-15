from rest_framework import generics, permissions
from django.contrib.auth import get_user_model
from user.api.serializers import RegisterSerializer

User = get_user_model()


class RegisterAPIView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    queryset = User.objects.all()

