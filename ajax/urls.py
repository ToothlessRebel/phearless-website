__author__ = 'ToothlessRebel'

from . import views
from django.conf.urls import url

urlpatterns = [
    url(r'^username_exists/(?P<username>.+?)/?$', views.check_username, name='username_exists'),
    url(r'^parse_api/?$', views.parse_api, name='parse_api')
]
