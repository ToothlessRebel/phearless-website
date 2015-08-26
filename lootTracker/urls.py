__author__ = 'ToothlessRebel'

from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index, name='index')
]