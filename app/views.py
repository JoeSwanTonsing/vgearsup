# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,logout
from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.db.models import Q

from .models import *

# Create your views here.
def index(request):
	categories = Category.objects.all().order_by('title')
	return render(request, 'app/index.html', {'categories' : categories})

def getstarted(request):
	return render(request, 'app/getstarted.html')

@login_required(login_url='/getstarted/')
def instrumentlist(request):
	return render(request, 'app/instrumentlist.html')

@login_required(login_url='/getstarted/')
def mymessages(request):
	user = request.user.appuser
	contacts = user.contactlist.all()
	ctx={
		'contacts':contacts
	}
	return render(request, 'app/messages.html',ctx)

@login_required(login_url='/getstarted/')
def chat(request,user2):
	user = request.user.appuser
	user2 = AppUser.objects.get(id=user2)
	contacts = user.contactlist.all()
	try:
		msgs = ChatMessage.objects.filter(Q(sender__id=user.id, receiver__id=user2.id) | Q(sender__id=user2.id, receiver__id=user.id)).order_by('timestamp')
	except ChatMessage.DoesNotExist:
		msgs = None
	ctx={
		'msgs':msgs,
		'user2':user2,
		'contacts':contacts
	}
	return render(request, 'app/chat.html',ctx)

@login_required(login_url='/getstarted/')
def chat_post(request, user2):	
	#u1 is sender, u2 is the receiver
	u1 = request.user.appuser
	u2 = AppUser.objects.get(id=user2)
	contacts = request.user.appuser.contactlist.all()
	if u2 not in u1.contactlist.all():
		# u2 is not yet in u1's contact list. So Add u2 to u1.
		# also add u1 to u2's contact list.
		try:
			u2.contactlist.add(u1)
			u2.save()
			u1.contactlist.add(u2)
			u1.save()
		except Exception as e:
			raise e
	else:
		print('No need to add')

	msg = ChatMessage.objects.create(sender=u1, receiver=u2)
	text = request.POST.get('chat')
	text_msg = ChatText.objects.create(message=msg, text=text)
	return HttpResponse("success")

@login_required(login_url='/getstarted/')
def chat_poll(request, user2, msg_id):
	u1 = request.user.appuser
	u2 = AppUser.objects.get(id=user2)

	msgs=ChatMessage.objects.filter(
				Q(id__gt=msg_id),
				Q(sender__id=u1.id, receiver__id=u2.id) |
				Q(sender__id=u2.id, receiver__id=u1.id)).order_by('timestamp')

	ctx={
		'msgs':msgs
	}
	return render (request,'app/chat2.html',ctx)

@login_required(login_url='/getstarted/')
def addnewcategoryaction(request):
	title=request.POST.get('cat_title')
	cat_image=request.FILES.get('cat_photo')
	categ=Category.objects.create(
		title=title,
		cat_image=cat_image
	)
	return redirect('/home/')

@login_required(login_url='/getstarted/')
def addnewbrandaction(request):
	name=request.POST.get('br_name')
	brn=Brand.objects.create(
		name=name
	)
	return redirect('/home/')

def category(request,cat_id):
	instcat=Category.objects.get(id=cat_id)
	instrument=Instrument.objects.filter(category=instcat).order_by('id')
	adcount= Instrument.objects.filter(category=instcat).count()
	return render(request, 'app/instrumentlist.html',{'instrument': instrument,'adcount':adcount,'instcat':instcat})

def viewproducts(request,inst_id):
	inst=Instrument.objects.filter(id=inst_id)
	instcat=Instrument.objects.get(id=inst_id)
	cat=instcat.category
	related_items = Instrument.objects.filter(category=cat).exclude(id=inst_id)
	adcount= Instrument.objects.filter(category=cat).count()
	# fav=Favourite.objects.filter(id=user)
	
	return render(request, 'app/viewproducts.html',{'inst':inst,'related_items':related_items,'adcount':adcount})

@login_required(login_url='/getstarted/')
def home(request):
	user=request.user.appuser
	categories = Category.objects.all().order_by('title')
	brands = Brand.objects.all().order_by('name')
	myads=Instrument.objects.filter(seller=user)
	adcount= Instrument.objects.filter(seller=user).count()
	try:
		fav=Favourite.objects.get(user=user)
	except Favourite.DoesNotExist:
		fav = None

	ctx={'categories' : categories,'brands':brands,'adcount':adcount,'myads':myads,'fav':fav}
	return render(request, 'app/home.html',ctx)

@login_required(login_url='/getstarted/')
def viewmyad(request,myad_id):
	user=request.user.appuser
	inst=Instrument.objects.filter(id=myad_id)
	adcount = Instrument.objects.filter(seller=user).count()
	related_items = Instrument.objects.filter(seller=user).exclude(id=myad_id)
	return render(request, 'app/viewmyad.html',{'inst': inst,'related_items':related_items,'adcount':adcount})

@login_required(login_url='/getstarted/')
def editprofile(request):
	return render(request, 'app/edit_profile.html')

def register_action(request):
	username=request.POST.get('username')
	password=request.POST.get('password')
	c_pass = request.POST.get('pass2')
	firstname=request.POST.get('firstname')
	lastname=request.POST.get('lastname')
	email=request.POST.get('email')
	phone=request.POST.get('phone')
	if password==c_pass:
		if User.objects.filter(username=username).exists():
			messages.error(request, 'Username already exists. Please login with the same credentials or choose a different username.')
			return redirect('/getstarted/')
		else:
			user=User.objects.create_user(
				username=username,
				password=password,
				first_name=firstname,
				last_name=lastname,
				email=email)
			app_user = AppUser.objects.create(
				user=user,
				contact=phone)
			fav = Favourite.objects.create(
				user=app_user
			)
			user = authenticate(request, username=username, password=password)

			if user is not None:
				login(request, user)
				messages.success(request, 'Hello ' + request.user.username + '!! Welcome to VGearsup.')
				return redirect('/home/')
			else:
				messages.error(request, 'An error occured. Please try again later.')
				return redirect('/getstarted/')
	else:
		messages.error(request, 'Passwords do not match.')
		return redirect('/getstarted/')

def login_action(request):
    #authenticate the user
	username= request.POST.get('username')
	password= request.POST.get('password')
	user = authenticate(request, username=username, password=password)
	if user is not None:
		login(request, user)
		messages.success(request, 'Hi there ' + request.user.username + '! Welcome back.')
		return redirect('/home/', {'messages' : messages})
	else:
		messages.error(request, 'Username and Password do not match. Please enter correct credentials.')
		return redirect('/getstarted/',{'messages' : messages})

@login_required(login_url='/getstarted/')
def logout_action(request):
	logout(request)
	messages.success(request, 'You have successfully logged out.')
	return redirect('/',{'messages':messages})

@login_required(login_url='/getstarted/')
def edit_profile_action(request):		
	first_name = request.POST.get('firstname')
	last_name = request.POST.get('lastname')
	username = request.POST.get('username')
	email = request.POST.get('email')
	phone = request.POST.get('phone')
	location = request.POST.get('location')
	cpassword = request.POST.get('conf_password')
	currpw = request.user.password
	user=request.user
	matchcheck = check_password(cpassword,currpw)
	if matchcheck:
		user.username=username
		user.first_name=first_name
		user.last_name=last_name
		user.email=email
		user.save()
		app_user = user.appuser
		app_user.contact=phone
		app_user.save()
		messages.success(request, 'Changes saved. Your Information has successfully be updated.')
		return redirect('/home/',{'messages' : messages})
	else:
		messages.error(request, 'Wrong Password entered. Please enter correct password.')
		return redirect('/editprofile/', {'messages' : messages})

@login_required(login_url='/getstarted/')
def changedp(request):
	user= request.user.appuser
	profile_photo=request.FILES.get('profile_photo')
	if profile_photo is not None:
		try:
			user.profile_pic=profile_photo
			user.save()
			messages.success(request, 'Profile Picture updated.')
			return redirect('/home/',{'messages':messages})
		except Exception as e:
			print e
		else:
			messages.success(request, 'There was a problem communicating with the server. Please try again later.')
			return redirect('/editprofile/',{'messages':messages})

@login_required(login_url='/login/')
def change_password(request):
	user=request.user
	current_password=request.POST.get('current_password')
	new_password=request.POST.get('new_password')
	confirm_new_password=request.POST.get('confirm_new_password')
	username=request.user.username
	#check if new_password and confirm_password are same
	if new_password==confirm_new_password:
		#check if user's provided password is same as the active password
		currpw = request.user.password
		matchcheck = check_password(current_password,currpw)
		if matchcheck:
			#if passwords match, then update the user's password to new password
			try:
				if new_password.strip():
					#strip removes leading and trailing whitespaces
					user.set_password(new_password)
				user.save()
				if user is not None:
					loginuser = authenticate(request, username=username, password=new_password)
					login(request, loginuser)
				messages.success(request,'Your account password has successfully been changed.')
				return redirect('/editprofile/',{'messages':messages})
			except Exception as e:
				messages.error(request,'There was a problem with the server. Please try again.')
				return redirect('/editprofile/',{'messages':messages})
		else:
			#if user's provided password is not same as the active password
			messages.error(request,'You have provided wrong password. Password is not updated.')
			return redirect('/editprofile/',{'messages':messages})
	else:
		messages.error(request,'New Password does not match with the Confirmed Password.')
		return redirect('/editprofile/',{'messages':messages})

@login_required(login_url='/getstarted/')
def postadaction(request):
	name=request.POST.get('name')
	price=request.POST.get('price')
	auction=request.POST.get('optauc')
	seller=request.user.appuser
	description=request.POST.get('description')
	photo=request.FILES.get('inst_photo')
	category_id=request.POST.get('inst_cat')
	category=Category.objects.get(id=category_id)
	condition=request.POST.get('item_cond')
	brand_id=request.POST.get('inst_br')
	brand=Brand.objects.get(id=brand_id)
	bid_end = request.POST.get('end_date')
	if auction == 'Yes':
		auctionpost = Auction.objects.create(
			name=name,
			seller=seller,
			bid_price=price,
			description=description,
			photo=photo,
			category=category,
			condition=condition,
			brand=brand,
			bid_end=bid_end
		)
		messages.success(request, 'Auction item has been created and posted.')
		return redirect('/home/#nav-myads', {'messages' : messages})
	else:
		adpost=Instrument.objects.create(
			name=name,
			price=price,
			seller=seller,
			description=description,
			photo=photo,
			category=category,
			condition=condition,
			brand=brand
		)
		messages.success(request, 'AD has been posted.')
		return redirect('/home/', {'messages' : messages})

@login_required(login_url='/getstarted/')
def addtofavouritesaction(request,inst_id):
	user=request.user.appuser
	inst=Instrument.objects.get(id=inst_id)
	iname=inst.name
	try:
		fav = Favourite.objects.get(user=user)
		fav.instruments.add(inst)
		msg='You have added ' + iname + ' to Favourites.'
		messages.success(request,msg)
		return redirect('/home/',{'messages':messages})
	except Exception as e:
		msg='Could not add ' + iname + ' to Favourites.'
		messages.error(request,e)
		return redirect('/home/',{'messages':messages})

@login_required(login_url='/getstarted/')
def removefavouritesaction(request, inst_id):
	user=request.user.appuser
	inst = Instrument.objects.get(id=inst_id)
	iname=inst.name
	try:
		fav = Favourite.objects.get(user=user)
		fav.instruments.remove(inst)
		msg='You have removed '+ iname + ' from your Favourites.'
		messages.success(request, msg)
		return redirect('/home/', {'messages':messages})
	except Exception as e:
		msg='Unable to remove '+ iname + ' from your Favourites. Please try again later.'
		messages.error(request, msg)
		return redirect('/home/', {'messages':messages})

@login_required(login_url='/getstarted/')
def editad(request, adid):
	user = request.user.appuser
	#check if user is the one that posted the ad, else dont allow
	instrument = Instrument.objects.get(id=adid)
	if instrument.seller == user:
		#if seller and user are same, allow to make changes to the ad
		#passing required values and objects
		categories=Category.objects.all()
		brands=Brand.objects.all()
		ctx={
			'categories':categories,
			'brands':brands,
			'instrument':instrument
		}
		return render(request,'app/editad.html',ctx)
	else:
		messages.error(request, 'You do not own the AD post, hence you do not have permission to edit the post.')
		ctx={'messages':messages}
		return redirect('/home/',ctx)

@login_required(login_url='/getstarted/')
def editad_action(request, adid):
	ad = Instrument.objects.get(id=adid)
	itemname = ad.name
	#get the new values from the form
	name=request.POST.get('name')
	price=request.POST.get('price')
	description=request.POST.get('description')
	photo=request.FILES.get('inst_photo')
	category_id=request.POST.get('inst_cat')
	category=Category.objects.get(id=category_id)
	condition=request.POST.get('item_cond')
	brand_id=request.POST.get('inst_br')
	brand=Brand.objects.get(id=brand_id)
	try:
		#if all is correct, then make changes to the entries in the database
		ad.name=name
		ad.price=price
		ad.description=description
		ad.category=category
		ad.brand=brand
		ad.condition=condition
		if photo is not None:
			ad.photo=photo
		ad.save() 
		messages.success(request,'You have updated AD details.')
		return redirect('/home/',{'messages':messages})
	except Exception as e:
		messages.error(request,'Unable to make changes. Please try again later.')
		return redirect('/home/',{'messages':messages})

@login_required(login_url='/getstarted/')
def auctions(request):
	items = Auction.objects.all()

	ctx={'items':items}
	return render(request,'app/auctions.html',ctx)

@login_required(login_url='/getstarted/')
def viewauction(request,inst_id):
	inst=Auction.objects.filter(id=inst_id)
	instcat=Auction.objects.get(id=inst_id)
	cat=instcat.category
	related_items = Auction.objects.filter(category=cat).exclude(id=inst_id)
	adcount= Auction.objects.filter(category=cat).count()
	# fav=Favourite.objects.filter(id=user)
	
	return render(request, 'app/viewproducts.html',{'inst':inst,'related_items':related_items,'adcount':adcount})

@login_required(login_url='/getstarted/')
def auction_bid_action(request,inst_id):
	items = Auction.objects.all()

	this_item = Auction.objects.get(id=inst_id)
	amt = request.POST.get('bid_amount')

	if amt > this_item.highest_bid_amount:
		try:
			this_item.highest_bid_amount=amt
			this_item.highest_bidder=request.user.appuser
			this_item.save()
		except Exception as e:
			raise e

	ctx={'items':items}
	return render(request,'app/auctions.html',ctx)

@login_required(login_url='/getstarted/')
def deletead(request,ad_id):
	user=request.user.appuser
	ad = Instrument.objects.get(id=ad_id)
	#if user is the seller, then allow to delete else dont allow:
	if ad.seller==user:
		try:
			ad.delete()
			messages.success(request,'AD item deleted')
			return redirect('/home/',{'messages':messages})
		except Exception as e:
			messages.success(request,'Error deleting AD item')
			return redirect('/home/',{'messages':messages})
	else:
		messages.success(request,'You are not allowed to delete ads that are not posted by you')
		return redirect('/home/',{'messages':messages})

@login_required(login_url='/getstarted/')
def user_information(request,user_id):
	user2 = AppUser.objects.get(id=user_id)
	u2_fav = Favourite.objects.get(user=user2)
	u2_ads = Instrument.objects.filter(seller=user2)
	adcount = Instrument.objects.filter(seller=user2).count()
	ctx={
		'user2':user2,
		'u2_fav':u2_fav,
		'u2_ads':u2_ads,
		'adcount':adcount
	}
	return render(request,'app/viewuser.html',ctx)