from django.conf.urls import url
from activities import views

urlpatterns = [
    url(r'^api/activities$', views.activity_list),
    url(r'^api/activities/(?P<pk>[0-9]+)$', views.activity_detail),
    url(r'^api/activity_sync$', views.activity_sync),
    url(r'^api/register_webhook$', views.register_webhook),
    url(r'^api/receive_webhook$', views.receive_webhook),
    url(r'^api/webhooks$', views.webhooks),
    url(r'^api/webhook/(?P<pk>[0-9]+)$', views.webhooks),
]
