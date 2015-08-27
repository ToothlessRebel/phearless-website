__author__ = 'ToothlessRebel'

from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^user/logout/?$', views.logout, name='logout'),
	url(r'^user/login/?$', views.login, name='login'),
	url(r'^user/signup/?$', views.signup, name='signup')
]
