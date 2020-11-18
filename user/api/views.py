from rest_framework import generics, status
from django.contrib.auth import get_user_model
from rest_framework.response import Response

from user.api.serializers import RegisterSerializer, SignupSerializer, MyTokenObtainPairSerializer

User = get_user_model()


class RegisterAPIView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    queryset = User.objects.all()

    def post(self, request, *args, **kwargs):
        serialized_user = SignupSerializer(data=request.data)
        if serialized_user.is_valid():
            User.objects.create_user(
                serialized_user.initial_data['email'],
                serialized_user.initial_data['email'],
                serialized_user.initial_data['password']
            )
            request.data.update({'username': request.data.get('email', {})})
            tokens = MyTokenObtainPairSerializer(request.data).validate(request.data)
            return Response(tokens, status=status.HTTP_201_CREATED)
        else:
            return Response(serialized_user._errors, status=status.HTTP_400_BAD_REQUEST)
