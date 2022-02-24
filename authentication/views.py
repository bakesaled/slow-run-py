from lib2to3.pgen2.tokenize import TokenError
from os import stat
from rest_framework import status, viewsets
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.exceptions import InvalidToken

# from django.conf import settings
# from django.middleware import csrf
# from django.contrib.auth import authenticate

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


class LoginAPIView(TokenObtainPairView):
  permission_classes = (AllowAny,)
  serializer_class = LoginSerializer

  def post(self, request):
    user_data = request.data.get('user', {})

    serializer = self.serializer_class(data=user_data)

    try:
      serializer.is_valid(raise_exception=True)
    except TokenError as e:
      raise InvalidToken(e.args[0])

    return Response(serializer.validated_data, status=status.HTTP_200_OK)


class LogoutAPIView(APIView):
  permission_classes = (IsAuthenticated,)

  def post(self, request):
    refresh_token = request.data['refresh_token']
    token = RefreshToken(refresh_token)
    token.blacklist()

    return Response(status=status.HTTP_205_RESET_CONTENT)


class RefreshAPIView(TokenRefreshView):
  permission_classes = (AllowAny,)
  http_method_names = ['post']

  def create(self, request, *args, **kwargs):
    serializer = self.get_serializer(data=request.data)
