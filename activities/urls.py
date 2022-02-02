from django.conf.urls import url
from activities import views

app_name = 'activities'

urlpatterns = [
    url(r'^activities$', views.activity_list),
    url(r'^activities/(?P<pk>[0-9]+)$', views.activity_detail),
    url(r'^activity_sync$', views.activity_sync),
    url(r'^register_webhook$', views.register_webhook),
    url(r'^receive_webhook$', views.receive_webhook),
    url(r'^webhooks$', views.webhooks),
    url(r'^webhook/(?P<pk>[0-9]+)$', views.webhook),
]
