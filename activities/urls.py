from django.conf.urls import url 
from activities import views 
 
urlpatterns = [ 
    url(r'^api/activities$', views.activity_list),
    url(r'^api/activities/(?P<pk>[0-9]+)$', views.activity_detail)
]