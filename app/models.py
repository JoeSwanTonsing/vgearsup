# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class AppUser(models.Model):
	user=models.OneToOneField(User,null=True)
	profile_pic = models.ImageField(upload_to='profile_pics/', default="profile_pics/default.png")
	contact=models.CharField(max_length=10,default='')
	location=models.CharField(max_length=50,default='')
	contactlist=models.ManyToManyField('self', null=True)

	def __str__(self):
		return str(self.user)

class Category(models.Model):
	title=models.CharField(max_length=50,default="")
	cat_image = models.ImageField(upload_to="cat_image/", null=True)
	def __str__(self):
		return str(self.title)

class Brand(models.Model):
	name=models.CharField(max_length=50,default="")
	def __str__(self):
			return str(self.name)

class Instrument(models.Model):
	name=models.CharField(max_length=50,default="")
	price=models.CharField(max_length=50,default="")
	seller=models.ForeignKey(AppUser,null=True,related_name='seller')
	description=models.CharField(max_length=150,default="")
	photo=models.ImageField(upload_to='instruments/', default="instruments/instruments.jpg")
	category=models.ForeignKey(Category,null=True)
	CND=[
		('Used','Used'),
		('New','New'),
	]
	condition=models.CharField(choices=CND,max_length=50,default="Used")
	brand=models.ForeignKey(Brand,null=True)
	timestamp=models.DateTimeField(auto_now_add=True,null=True)

	def __str__(self):
		return str(self.name)

class Auction(models.Model):
	name=models.CharField(max_length=50,default="")
	price=models.CharField(max_length=50,default="")
	seller=models.ForeignKey(AppUser,null=True,related_name='auction_seller')
	description=models.CharField(max_length=150,default="")
	photo=models.ImageField(upload_to='instruments/', default="instruments.jpg")
	category=models.ForeignKey(Category,null=True)
	timestamp=models.DateTimeField(auto_now_add=True,null=True)
	CND=[
		('Used','Used'),
		('New','New'),
	]
	condition=models.CharField(choices=CND,max_length=50,default="Used")
	brand=models.ForeignKey(Brand,null=True)
	bid_end =models.DateTimeField(auto_now=False,null=True)
	highest_bid_amount=models.CharField(max_length=10,default="")
	highest_bidder=models.ForeignKey(AppUser,null=True,related_name='highest_bidder')
	def __str__(self):
		return str(self.name)

class Favourite(models.Model):
	instruments=models.ManyToManyField(Instrument)
	user=models.ForeignKey(AppUser,null=True,related_name='favuser')
	timestamp=models.DateTimeField(auto_now_add=True,null=True)
	def __str__(self):
		return str(self.user)

class ChatMessage(models.Model):
	sender=models.ForeignKey(AppUser,null=True,related_name='sender')
	receiver=models.ForeignKey(AppUser,null=True,related_name='receiver')
	timestamp=models.DateTimeField(auto_now_add=True,null=True)

	def __str__(self):
		return str(self.timestamp) + '__'+str(self.sender) + ' - ' +  str(self.receiver)

class ChatText(models.Model):
	message = models.OneToOneField(ChatMessage, null=True)
	text=models.TextField(default='')

	def __str__(self):
		return str(self.message)