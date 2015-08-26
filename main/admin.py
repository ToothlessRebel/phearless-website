from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import Api

# Register your models here.


class ApiInline(admin.StackedInline):
	model = Api
	can_delete = False
	verbose_name = 'API Key'
	verbose_name_plural = 'API Keys'


class ApiAdmin(UserAdmin):
	inlines = (ApiInline,)

admin.site.unregister(User)
admin.site.register(User, ApiAdmin)
