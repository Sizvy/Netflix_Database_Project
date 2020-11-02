from django.shortcuts import render,redirect
from django.db import connection
import re
from django.http import HttpResponse
# Create your views here.

logged_in = False
ID = -1

def home_notLoggedIn(response):
    return redirect("http://127.0.0.1:8000/user/login")

def home_LoggedIn(request,user_ID):
    #Home page specific to user
    return HttpResponse('This is User_ID'+str(user_ID))


