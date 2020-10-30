from django.shortcuts import render,redirect
from django.db import connection
import re
# Create your views here.

logged_in = False
ID = -1

def home(response):
    if logged_in == False:
        return redirect("http://127.0.0.1:8000/user/login")
