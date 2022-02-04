from os import stat
from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework_simplejwt.tokens import RefreshToken

from django.conf import settings
from django.middleware import csrf
from django.contrib.auth import authenticate

from .serializers import LoginSerializer, RegistrationSerializer, UserSerializer
from .renderers import UserJSONRenderer


class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
  permission_classes = (IsAuthenticated,)
  renderer_classes = (UserJSONRenderer,)
  serializer_class = UserSerializer

  def retrieve(self, request, *args, **kwargs):
    serializer = self.serializer_class(request.user)

    return Response(serializer.data, status=status.HTTP_200_OK)

  def update(self, request, *args, **kwargs):
    user_data = request.data.get('user', {})

    serializer_data = {
        'username': user_data.get('username', request.user.username),
        'email': user_data.get('email', request.user.email),
        'profile': {
            'bio': user_data.get('bio', request.user.profile.bio),
            'image': user_data.get('image', request.user.profile.image)
        }
    }

    serializer = self.serializer_class(
        request.user, data=serializer_data, partial=True
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()

    return Response(serializer.data, status=status.HTTP_200_OK)


class RegistrationAPIView(APIView):
  permission_classes = (AllowAny,)
  renderer_classes = (UserJSONRenderer,)
  serializer_class = RegistrationSerializer

  def post(self, request):
    user = request.data.get('user', {})

    serializer = self.serializer_class(data=user)
    serializer.is_valid(raise_exception=True)
    serializer.save()

    return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginAPIView(APIView):
  permission_classes = (AllowAny,)
  renderer_classes = (UserJSONRenderer,)
  serializer_class = LoginSerializer

  def post(self, request):
    user_data = request.data.get('user', {})

    serializer = self.serializer_class(data=user_data)
    serializer.is_valid(raise_exception=True)
    email = request.data.get('user', dict()).get('email')
    password = request.data.get('user', dict()).get('password')
    user = authenticate(username=email, password=password)

    data = get_tokens_for_user(user)

    response = Response()
    response.set_cookie(
        key=settings.SIMPLE_JWT['AUTH_COOKIE'],
        value=data["access"],
        expires=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
        secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
        httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
        samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
    )
    csrf.get_token(request)
    response.data = {
        "Successs": "Login Successful",
        "data": data
    }
    response.status_code = status.HTTP_200_OK

    return response


def get_tokens_for_user(user):
  refresh = RefreshToken.for_user(user)
  return {
      'refresh': str(refresh),
      'access': str(refresh.access_token),
  }
