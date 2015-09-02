from . import views
from django.conf.urls import url

urlpatterns = [
    url(r'^username_exists/(?P<username>.+?)/?$', views.check_username, name='username_exists'),
    url(r'^parse_api/?$', views.parse_api, name='parse_api'),
    url(r'^name_to_id/(?P<item_name>.+?)/?$', views.item_name_to_id),
    url(r'^add_drop_to_fleet/(?P<fleet_id>\d+?)/(?P<item_id>\d+?)/(?P<quantity>\d+?)/?$', views.add_drop_to_fleet),
    url(r'^fleet_member_icons/(?P<fleet_id>\d+?)/?$', views.fleet_member_icons),
    url(r'^load_loot_table/(?P<fleet_id>\d+?)/?$', views.load_loot_table)
]
