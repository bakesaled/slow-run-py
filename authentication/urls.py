from django.conf.urls import url
from django.urls import path
from authentication.views import RefreshAPIView, LoginAPIView, LogoutAPIView, RegistrationAPIView, UserRetrieveUpdateAPIView

app_name = 'authentication'

urlpatterns = [
    path('user', UserRetrieveUpdateAPIView.as_view()),
    path('users', RegistrationAPIView.as_view()),
    path('users/login', LoginAPIView.as_view()),
    path('users/login/refresh', RefreshAPIView.as_view(), name='token_refresh'),
    path('users/logout', LogoutAPIView.as_view()),
]
