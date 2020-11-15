from rest_framework import serializers

from django.contrib.auth.models import User


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password']

    def create(self, validated_data):
        validated_data.update({'username': validated_data.get('email')})
        return super(RegisterSerializer, self).create(validated_data)