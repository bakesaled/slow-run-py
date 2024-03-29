from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from django.contrib.auth import authenticate

from profiles.serializers import ProfileSerializer
from .models import User


class RegistrationSerializer(serializers.ModelSerializer):
  password = serializers.CharField(
      max_length=128,
      min_length=8,
      write_only=True
  )

  token = serializers.CharField(max_length=255, read_only=True)

  class Meta:
    model = User

    # include all fields that could possibly be incldued in a request
    fields = ['email', 'username', 'password', 'token']

  def create(self, validated_data):
    return User.objects.create_user(**validated_data)


class LoginSerializer(TokenObtainPairSerializer):
  email = serializers.CharField(max_length=255)
  username = serializers.CharField(max_length=255, read_only=True)
  password = serializers.CharField(max_length=128, write_only=True)
  token = serializers.CharField(max_length=255, read_only=True)

  def validate(self, attrs):
    data = super().validate(attrs)

    refresh = self.get_token(self.user)

    data['user'] = UserSerializer(self.user).data
    data['refresh'] = str(refresh)
    data['access'] = str(refresh.access_token)

    return data


class UserSerializer(serializers.ModelSerializer):
  password = serializers.CharField(
      max_length=128,
      min_length=8,
      write_only=True
  )

  profile = ProfileSerializer(write_only=True)
  bio = serializers.CharField(source='profile.bio', read_only=True)
  image = serializers.CharField(source='profile.image', read_only=True)

  class Meta:
    model = User
    fields = ('email', 'username', 'password',
              'profile', 'bio', 'image',)

  def update(self, instance, validated_data):
    # remove password from fields because it is hashed
    password = validated_data.pop('password', None)

    profile_data = validated_data.pop('profile', {})

    for (key, value) in validated_data.items():
      setattr(instance, key, value)

    if password is not None:
      # sepcial security stuff
      instance.set_password(password)

    instance.save()

    for (key, value) in profile_data.items():
      setattr(instance.profile, key, value)

    instance.profile.save()

    return instance
