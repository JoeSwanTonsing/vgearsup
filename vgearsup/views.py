from django.contrib.auth import authenticate, login,logout
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta

from .models import *