from django.shortcuts import render,redirect
from django.db import connection
import re
from django.http import HttpResponse
# Create your views here.

logged_in = False
ID = -1

def home_notLoggedIn(request):
    if request.session.get('is_logged_in',False) == True:
        #return HttpResponse('This is User_ID' + request.session.get('user_ID',-1))
        return render(request, "home/home.html")
    else:
        return redirect("http://127.0.0.1:8000/user/login")

def home_LoggedIn(request,user_ID):
    #Home page specific to user
    print(user_ID)

    if 'is_logged_in' in request.session:
        if user_ID == request.session.get('user_ID',-1) and request.session.get('is_logged_in', False) == True:
            #return HttpResponse('This is User_ID' + str(user_ID))
            return render(request,"home/home.html")
        else:
            print("not logged in")
            return redirect("http://127.0.0.1:8000/user/login/")

    else:
        print("not logged in")
        return redirect("http://127.0.0.1:8000/user/login/")

def log_out(request):
    print("here")

    if request.session.get('is_logged_in',False) == True:
        try:
            del request.session['user_ID']
            del request.session['is_logged_in']
        except KeyError:
            pass
        print("logged out successfully")

    return redirect("http://127.0.0.1:8000/user/login")








