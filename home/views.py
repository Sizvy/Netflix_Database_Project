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
        id = request.session.get('user_ID', -1)
        cursor = connection.cursor()
        sql = "SELECT * FROM USERS WHERE USER_ID = %s"
        cursor.execute(sql, id)
        result = cursor.fetchall()
        cursor.close()
        for r in result:
            first_name = r[2]
        cursor = connection.cursor()
        sql = "SELECT * FROM SHOW"
        cursor.execute(sql)
        result_show = cursor.fetchall()
        cursor.close()
        show_list = []
        for r in result_show:
            show_title = r[2]
            show_genre = r[1]
            show_imdb = r[5]
            show_image = r[13]
            single_row = {"show_title": show_title, "show_genre": show_genre, "show_imdb": show_imdb,
                          "show_image": show_image}
            show_list.append(single_row)


        return render(request, "home/homepage.html", {'shows': show_list})

    else:
        return redirect("http://127.0.0.1:8000/user/login")

#not used anymore, might use in future
def home_LoggedIn(request,user_ID):
    #Home page specific to user
    print(user_ID)

    if 'is_logged_in' in request.session:
        if user_ID == request.session.get('user_ID',-1) and request.session.get('is_logged_in', False) == True:
            #return HttpResponse('This is User_ID' + str(user_ID))
            return render(request,"home/homepage.html")
        else:
            print("not logged in")
            return redirect("http://127.0.0.1:8000/user/login/")

    else:
        print("not logged in")
        return redirect("http://127.0.0.1:8000/user/login/")


def search(request):

    search_item = request.GET.get('search')

    search_pattern = "%"+search_item.lower()+"%"

    print(search_item)

    cursor = connection.cursor()
    sql = "SELECT DISTINCT(s.SHOW_ID) FROM SHOW s, DIRECTOR d,ACTOR a,ACT ac" \
          " WHERE s.DIRECTOR_ID = d.PERSON_ID" \
          " AND s.SHOW_ID = ac.SHOW_IDACT AND ac.ACTOR_IDACT = a.PERSON_ID AND " \
          "(" \
          "LOWER(s.TITLE) like %s" \
          " OR LOWER(d.DIRECTOR_FIRST_NAME || '' || d.DIRECTOR_LAST_NAME) like %s" \
          " OR LOWER(a.ACTOR_FIRST_NAME || '' || a.ACTOR_LAST_NAME) like %s" \
          " OR LOWER(s.GENRE) like %s)"

    print(sql)

    cursor.execute(sql, [search_pattern, search_pattern, search_pattern, search_pattern])
    result = cursor.fetchall()
    cursor.close()

    error_msg = "No Result Found!"
    show_list=[]
    for r in result:

        show_id = r[0]
        print(show_id)
        cursor = connection.cursor()
        sql = 'SELECT * FROM SHOW WHERE SHOW_ID = %s'
        cursor.execute(sql, [show_id])
        show_res = cursor.fetchall()
        cursor.close()

        for r_temp in show_res:
            show_title = r_temp[2]
            show_genre = r_temp[1]
            show_des = r_temp[3]
            show_age = r_temp[4]
            show_lang = r_temp[8]
            show_image = r_temp[13]
            show_imdb = r_temp[5]
            single_row = {"show_imdb": show_imdb,
                          "show_title": show_title,
                          "show_genre": show_genre,
                          "show_des": show_des,
                          "show_age": show_age,
                          "show_lang": show_lang,
                          "show_image": show_image}
            show_list.append(single_row)
            error_msg = ""


    show_all = {
        "show_name":search_item,
        "shows":show_list,
        "error_msg":error_msg
    }
    return render(request, 'home\homepage.html', {'shows': show_list , 'error_msg': error_msg})




def log_out(request):
    if request.session.get('is_logged_in',False) == True:
        try:
            del request.session['user_ID']
            del request.session['is_logged_in']
        except KeyError:
            pass
        print("logged out successfully")

    return redirect("http://127.0.0.1:8000/user/login")











