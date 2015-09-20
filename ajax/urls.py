from . import views
from django.conf.urls import url

urlpatterns = [
    url(r'^username_exists/(?P<username>.+?)/?$', views.check_username, name='username_exists'),
    url(r'^parse_api/?$', views.parse_api, name='parse_api'),
    url(r'^name_to_id/(?P<item_name>.+?)/?$', views.item_name_to_id),
    # Fleet routes
    url(r'^fleets/?$', views.load_fleets),
    url(r'^fleets/create/?$', views.create_fleet),
    url(r'^fleet/(?P<fleet_id>\d+?)/add_drop/(?P<item_id>\d+?)/(?P<quantity>\d+?)/?$', views.add_drop_to_fleet),
    url(r'^fleet/(?P<fleet_id>\d+?)/member_icons/?$', views.fleet_member_icons),
    url(r'^fleet/(?P<fleet_id>\d+?)/loot_table/?$', views.load_loot_table),
    url(r'^fleet/(?P<fleet_id>\d+?)/finalize/?$', views.finalize_fleet),
]
