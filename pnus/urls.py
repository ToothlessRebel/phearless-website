from django.conf.urls import include, url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
import lootTracker

urlpatterns = [
    # Examples:
    # url(r'^$', 'pnus.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^loot/', include('lootTracker.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^ajax/', include('ajax.urls')),

    url(r'^', include('main.urls'))
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) \
  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
