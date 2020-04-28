# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(AppUser)
admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(Instrument)
admin.site.register(Favourite)
admin.site.register(ChatMessage)
admin.site.register(ChatText)
admin.site.register(Auction)