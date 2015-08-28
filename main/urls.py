__author__ = 'ToothlessRebel'

from . import views
from django.conf.urls import url

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^user/logout/?$', views.logout, name='logout'),
    url(r'^user/login/?$', views.login, name='login'),
    url(r'^user/signup/?$', views.signup, name='signup'),
    url(r'^user/characters/?$', views.pick_characters, name='pick_characters'),
    url(r'^user/set_character/(?P<character_id>.+?)/?$', views.set_character, name='set_character')
]
