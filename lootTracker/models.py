from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Item(models.Model):
	name = models.CharField(max_length=200)
	eve_id = models.BigIntegerField(unique=True)
	value = models.BigIntegerField()

	def __str__(self):
		return self.name


class Alliance(models.Model):
	name = models.CharField(max_length=200)
	eve_id = models.BigIntegerField(unique=True)
	portrait = models.FileField(upload_to='eve/portraits/alliance')

	def __str__(self):
		return self.name


class Corporation(models.Model):
	name = models.CharField(max_length=200)
	alliance = models.ForeignKey(Alliance)
	eve_id = models.BigIntegerField(unique=True)
	portrait = models.FileField(upload_to='eve/portraits/corporation')

	def __str__(self):
		return self.name


class Character(models.Model):
	name = models.CharField(max_length=200)
	corporation = models.ForeignKey(Corporation)
	eve_id = models.BigIntegerField(unique=True)
	user = models.ForeignKey(User, null=True)
	portrait = models.FileField(upload_to='eve/portraits/character')

	def __str__(self):
		return self.name


class Fleet(models.Model):
	corporation = models.ForeignKey(Corporation)
	members = models.ManyToManyField(Character)

	def __str__(self):
		return 'Fleet ' + str(self.id)


class Drop(models.Model):
	item = models.ForeignKey(Item)
	fleet = models.ForeignKey(Fleet)
	quantity = models.IntegerField()
	item_current_value = models.BigIntegerField()

	def __str__(self):
		return 'Drop ' + str(self.id)


class Treasury(models.Model):
	name = models.CharField(max_length=200, default='')
	corporation = models.ForeignKey(Corporation)
	value = models.BigIntegerField()

	def __str__(self):
		return self.corporation.name + ':' + self.name


class Payment(models.Model):
	treasury = models.ForeignKey(Treasury)
	character = models.ForeignKey(Character)
	value = models.BigIntegerField()

	def __str__(self):
		return 'Payment to ' + self.character.name + ' of ' + str(self.value) + ' ISK.'
