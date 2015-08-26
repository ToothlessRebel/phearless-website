__author__ = 'ToothlessRebel'

from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^username_exists/(?P<username>.+?)/?$', views.check_username, name='username_exists')
]