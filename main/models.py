from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Api(models.Model):
	user = models.OneToOneField(User)
	key = models.CharField(max_length=200)
	verification_code = models.CharField(max_length=200)