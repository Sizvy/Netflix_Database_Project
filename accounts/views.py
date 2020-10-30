from django.shortcuts import render,redirect
from django.db import connection
import re

logged_in = False


def is_valid(l):
    for i in l:
        if i == '':
            return False
    return True

def is_valid_email(e):
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'

    if re.search(regex,e):
        return True
    else:
        return False

def is_already_taken(e):
    cursor = connection.cursor()
    sql = "SELECT email FROM USERS"
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()

    for r in result:
        if e == r[0]:
            return True
    return False

def push_into_db(l):

    cursor = connection.cursor()
    sql_ID = "SELECT NVL(MAX(USER_ID),0) FROM USERS"
    cursor.execute(sql_ID)
    result = cursor.fetchall()
    for i in result:
        ID = i[0]
    cursor.close()
    ID = ID+1
    print(ID)


    cursor = connection.cursor()
    curr_date_sql = "SELECT TO_CHAR(SYSDATE, 'YYYY-MM-DD') FROM dual"
    curr_date_list = cursor.execute(curr_date_sql)
    for i in curr_date_list:
        curr_date = str(i[0])
    print(curr_date)
    cursor.close()


    cursor = connection.cursor()
    sql = "INSERT INTO USERS(USER_ID,USER_FIRSTNAME, USER_LASTNAME, GENDER, DATE_OF_BIRTH, EMAIL, PHONE_NO, PASSWORD, JOIN_DATE) VALUES(%s, %s, %s, %s, TO_DATE(%s,'DD/MM/YYYY'), %s, %s, %s, %s)"
    cursor.execute(sql, [ID, l[0], l[1], l[2], l[3], l[4], l[5], l[6], curr_date])
    connection.commit()
    cursor.close()


def register(response):
    error_msg = ""

    if response.method == "POST":
        print(response.POST)

        if response.POST.get("Register"):
            first_name = response.POST.get("first_name")
            last_name = response.POST.get("last_name")
            gender = ""
            if response.POST.get("gender"):
                gender = response.POST.get("gender")
            bday = response.POST.get("birthday")
            email = response.POST.get("email")
            phone = response.POST.get("phone")
            password = response.POST.get("password")
            conf_password = response.POST.get("confirm_password")

            l = []
            l.append(first_name)
            l.append(last_name)
            l.append(gender)
            l.append(bday)
            l.append(email)
            l.append(phone)
            l.append(password)
            l.append(conf_password)
            print(l)


            if is_valid(l) == False:
                print("No Field can be left empty")
                error_msg = "No Field can be left empty"

            else:
                if is_valid_email(email) == False:
                    print("Not a valid e-mail")
                    error_msg = "Not a valid e-mail"
                elif is_already_taken(email) == True:
                    print("email already used with an account")
                    error_msg = "email already used with an account"
                elif len(password) < 8:
                    print("Password should be at least 8 characters")
                    error_msg = "Password should be at least 8 characters"

                elif password != conf_password:
                    print("Passwords do not match")
                    error_msg = "Passwords do not match"
                else:
                    push_into_db(l)
                    logged_in = True
                    print("Successfully registered")
                    #redirect to login page
                    return redirect("http://127.0.0.1:8000/user/login/")


    return render(response, 'accounts\RegisterForm.html',{"error_msg":error_msg})




def login(response):

    cursor = connection.cursor()
    sql = "SELECT * FROM USERS"
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()

    error_msg = ""

    if response.method == "POST":
        print(response.POST)
        if response.POST.get("login"):
            email = response.POST.get("email")
            password = response.POST.get("password")
            print(email)
            print(password)

            ok = False
            for r in result:
                email_db = r[10]
                password_db = r[4]
                if email_db == email and password_db == password:
                    ok = True
                    break

            if ok == False:
                print("Wrong Email or Password. Try Again!")
                error_msg = "Wrong Email or Password. Try Again!"
            else:
                print("successfully logged in")
                #redirect to home page


    return render(response, 'accounts\loginForm.html',{"error_msg" : error_msg})