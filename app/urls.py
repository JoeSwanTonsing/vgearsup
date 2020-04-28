from django.conf.urls import url
from django.contrib import admin
from django.conf.urls.static import static
from . import views

app_name='app'
urlpatterns = [
	# gen
	url(r'^$',views.index,name='index'),
	url(r'^index/$',views.index,name='index'),
	url(r'^getstarted/$',views.getstarted,name='getstarted'),

	# User related links and actions
	url(r'^editprofile/$',views.editprofile,name='editprofile'),
	url(r'^edit_profile_action/$',views.edit_profile_action,name='edit_profile_action'),
	url(r'^changedp/$',views.changedp,name='changedp'),
	url(r'^change_password/$',views.change_password,name='change_password'),
	url(r'user_information/(?P<user_id>[0-9]+)$',views.user_information,name='user_information'),

	# AD and related actions and links
	url(r'^instrumentlist/$',views.instrumentlist,name='instrumentlist'),
	url(r'^addnewcategoryaction/$',views.addnewcategoryaction,name='addnewcategoryaction'),
	url(r'^addnewbrandaction/$',views.addnewbrandaction,name='addnewbrandaction'),
	url(r'^postadaction/$',views.postadaction,name='postadaction'),
	url(r'^editad/(?P<adid>[0-9]+)/$',views.editad,name='editad'),
	url(r'^editad_action/(?P<adid>[0-9]+)/$',views.editad_action,name='editad_action'),
	url(r'^viewmyad/(?P<myad_id>[0-9]+)/$',views.viewmyad,name='viewmyad'),
	url(r'^category/(?P<cat_id>[0-9]+)/$',views.category,name='category'),
	url(r'^viewproducts/(?P<inst_id>[0-9]+)/$',views.viewproducts,name='viewproducts'),
	url(r'^addtofavouritesaction/(?P<inst_id>[0-9]+)/$',views.addtofavouritesaction,name='addtofavouritesaction'),
	url(r'^removefavouritesaction/(?P<inst_id>[0-9]+)/$',views.removefavouritesaction,name='removefavouritesaction'),
	url(r'^deletead/(?P<ad_id>[0-9]+)/$',views.deletead,name='deletead'),
	url(r'^auctions/$',views.auctions,name='auctions'),
	url(r'^viewpauction/(?P<inst_id>[0-9]+)/$',views.viewauction,name='viewauction'),
	url(r'^auction_bid_action/(?P<inst_id>[0-9]+)/$',views.auction_bid_action,name='auction_bid_action'),

	# Messaging and Chats links and actions
	url(r'^mymessages/$',views.mymessages,name='mymessages'),
	url(r'^chat/(?P<user2>[0-9]+)/$',views.chat,name='chat'),
	url(r'^chat_post/(?P<user2>[0-9]+)/$',views.chat_post, name='chat_post'),
	url(r'^chat_poll/(?P<user2>[0-9]+)/(?P<msg_id>[0-9]+)/$',views.chat_poll, name='chat_poll'),

	# Register
	url(r'^register_action/$', views.register_action, name='register_action'),

	# Login and Logout
	url(r'^login_action/$', views.login_action, name='login_action'),
	url(r'^home/$',views.home,name='home'),
	url(r'^logout_action/$', views.logout_action, name='logout_action'),
]