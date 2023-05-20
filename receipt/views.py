from django.shortcuts import render,redirect
from urllib.request import urlopen
from django.http import JsonResponse
from receipt.models import Transaction2,Userregistration2,Signature2,Logo,Key,Tmpreg,Tmpforgetpassword
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User,auth
# from django.views.decorators.csrf import csrf_exempt
import matplotlib.pyplot as plt
from num2words import num2words
import numpy as np
import os
import requests
from django.test import Client

import datetime
from datetime import timedelta,date


from email.message import EmailMessage
import smtplib
import ssl


import string
import random

def error_404(request):
    return render(request, "404.html")

def index(request):
    return render(request,"user_registration.html")

@login_required(login_url="user_login")
def add_transaction(request):
    get_user = Userregistration2.objects.get(username = request.user.username[9:])
    company_name = get_user.businessname
    if request.method == "POST":
        receiver = request.POST['receiver_name']
        digit_naira = request.POST['digit_naira']
        # amount_naira = request.POST['amount_naira']
        
        if "." in digit_naira:
            x,y = digit_naira.split(".")
            naira = num2words(x)
            kobo = num2words(y)
            amount_naira = num2words(x).replace(",", "")+ " Naira " + num2words(y).replace(",", "")+ " Kobo"
        else:
            amount_naira = num2words(digit_naira).replace(",", "")+ " Naira Only"

        description = request.POST['description']
        username = request.user.username[9:]
        get_user = Userregistration2.objects.get(username = username)
        company_name = get_user.businessname
        
        if Logo.objects.filter(username = request.user.username[9:]).exists():
            get_logo = Logo.objects.get(username = request.user.username[9:])
            company_logo = get_logo.logo
        else:
            messages.info(request, "Please Upload a Logo First")
            return redirect("upload_logo")
        

        if Signature2.objects.filter(username = request.user.username[9:]).exists():
            get_signature = Signature2.objects.get(username = request.user.username[9:])
            signature = get_signature.signature
        else:
            messages.info(request, "Please Upload a Signature First")
            return redirect("upload_signature")
        
        datey = date.today()
        new_transaction = Transaction2(date = datey, receiver_name= receiver,amount_in_word_naira=amount_naira,description=description,amount_in_digit_naira=digit_naira, username = username)
        new_transaction.save()
        context = {
            "receiver":receiver,
            "amount_naira":amount_naira,
            # "amount_kobo":amount_kobo,
            "description":description,
            # "description2":description2,
            "digit_naira":digit_naira,
            # "digit_kobo":digit_kobo,
            "company_name":company_name,
            "company_logo":company_logo,
            "signature":signature,
            

        }
        return redirect("receipt/"+str(new_transaction.id))
    return render(request,"add_transaction.html",{"company_name":company_name})

@login_required(login_url="user_login")
def receipt(request,id):
    get_user = Userregistration2.objects.get(username = request.user.username[9:])
    company_name = get_user.businessname
    if Transaction2.objects.filter(id = id, username = request.user.username[9:]).exists():
        receipt_id = id
        transaction = Transaction2.objects.get(id = receipt_id)
        date = transaction.date
        receiver = transaction.receiver_name
        amount_naira = transaction.amount_in_word_naira
        description = transaction.description
        digit_naira = transaction.amount_in_digit_naira
        username = request.user.username[9:]
        get_user = Userregistration2.objects.get(username = username)
        company_name = get_user.businessname 
        get_logo = Logo.objects.get(username = username)
        company_address = get_user.businessaddress
        # company_logo = get_logo.logo
        company_logo = "../../media/businesslogo/"+request.user.username[9:]+".png"

        get_signature = Signature2.objects.get(username = username)
        signature = "../../media/signature/"+request.user.username[9:]+".png"
        context = {
                "receiver":receiver,
                "amount_naira":amount_naira,
                "description":description,
                "digit_naira":digit_naira,
                "company_name":company_name,
                "company_address":company_address,
                "company_logo":company_logo,
                "signature":signature,
                "date":date,
                "id":transaction.id,
                "company_name":company_name,
                "a":"../../media/signature/"+request.user.username[9:]+".png"
                

            }
        get_user = Userregistration2.objects.get(username = request.user.username[9:])
        receipt = get_user.receipt_type
        return render(request, receipt+".html",context)
    else:
        return render(request, "error_receipt.html",{"company_name":company_name})

@login_required(login_url="user_login")
def receipt2(request,id):
    get_user = Userregistration2.objects.get(username = request.user.username[9:])
    company_name = get_user.businessname
    if Transaction2.objects.filter(id = id, username = request.user.username[9:]).exists():
        receipt_id = id
        transaction = Transaction2.objects.get(id = receipt_id)
        date = transaction.date
        receiver = transaction.receiver_name
        amount_naira = transaction.amount_in_word_naira
        description = transaction.description
        digit_naira = transaction.amount_in_digit_naira
        username = request.user.username[9:]
        get_user = Userregistration2.objects.get(username = username)
        company_name = get_user.businessname 
        get_logo = Logo.objects.get(username = username)
        company_address = get_user.businessaddress
        company_logo = "../../media/businesslogo/"+request.user.username[9:]+".png"

        # company_logo = get_logo.logo
        get_signature = Signature2.objects.get(username = username)
        signature = "../../media/signature/"+request.user.username[9:]+".png"
        context = {
                "receiver":receiver,
                "amount_naira":amount_naira,
                "description":description,
                "digit_naira":digit_naira,
                "company_name":company_name,
                "company_address":company_address,
                "company_logo":company_logo,
                "signature":signature,
                "date":date,
                "id":transaction.id,
                "company_name":company_name
                

            }

        return render(request, "receipt2.html",context)
    else:
        return render(request, "error_receipt2.html",{"company_name":company_name})

def user_registration(request):

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        businessname = request.POST['businessname']
        businessaddress = request.POST['businessaddress']
        email = request.POST['email']
    

        if User.objects.filter(username="Business@"+username).exists():
            messages.info(request, "PLEASE USE ANOTHER USERNAME")
            return redirect("user_registration")
        else:
            check_exists = Tmpreg.objects.filter(username = username)
            if len(check_exists) == 1:
                check_exists.delete()

            characters = list(string.digits)
            random.shuffle(characters)

            code = []

            for x in range(6):
                code.append(random.choice(characters))
            random.shuffle(code)

            code = "".join(code)
            tmp_reg = Tmpreg(username = username, password = password, businessname = businessname, businessaddress = businessaddress, email = email, code = code)
            tmp_reg.save()

            sender = "adebimpeazeezniyi@gmail.com"
            receiver = email
            # body = """
            #     <h1>WELCOME BOSS</h1>
            # """
            body = "Your Verification Code is " + code
            subject = "Email Verification"
            password = 'hizcbuuvzjsreojr'

            # password = 'jhssqboljlaoukex'


            em = EmailMessage()
            em["From"] = sender
            em["To"] = receiver
            em["subject"] = subject
            em.set_content(body)

            context = ssl.create_default_context()

            with smtplib.SMTP_SSL("smtp.gmail.com",465,context=context) as smtp:
                smtp.login(sender,password)
                smtp.sendmail(sender,receiver,em.as_string())

            return redirect("verify_email/"+username)

            # user = User.objects.create_user(username = "Business@"+username, password = password)
            # user.save()
            # registration = Userregistration2(user = user, username = username, password = password, businessname = businessname, businessaddress = businessaddress)
            # registration.save()


            # user_login = authenticate(request, username = "Business@"+username, password = password)
            # if user_login is not None:
            #     login(request, user_login)
            #     messages.info(request, "REGISTRATION SUCCESSFUL")
            #     return redirect("add_transaction")
            # else:
            #     messages.info(request, "REGISTRATION NOT SUCCESSFUL")
            #     return redirect("user_registration")
    return render(request, "user_registration.html")

def verify_email(request,id):
    if request.method == "POST":
        code = request.POST['code']
        
        tmp_reg = Tmpreg.objects.get(username = id)
        username = tmp_reg.username
        password = tmp_reg.password
        businessname = tmp_reg.businessname
        businessaddress = tmp_reg.businessaddress
        email = tmp_reg.email
        dbcode = tmp_reg.code

        if code == dbcode:
            user = User.objects.create_user(username = "Business@"+username, password = password)
            user.save()
            registration = Userregistration2(user = user, username = username, password = password, businessname = businessname, businessaddress = businessaddress, email = email)
            registration.save()


            user_login = authenticate(request, username = "Business@"+username, password = password)
            if user_login is not None:
                login(request, user_login)
                messages.info(request, "REGISTRATION SUCCESSFUL")
                return redirect("add_transaction")
            else:
                messages.info(request, "REGISTRATION NOT SUCCESSFUL")
                return redirect("user_registration")
        else:
            messages.info(request, "INVALID ACTIVATION CODE")
            return redirect("../verify_email/"+username)



    return render(request, "verify_email.html")


def user_login(request):
    if request.method == "POST":
        username =  request.POST['username']
        password = request.POST['password']
        altusername = "business@"+username

        user_login = authenticate(request, username = "Business@" + username, password = password)
        if user_login is not None:
            login(request, user_login)
            return redirect("add_transaction")
        else:
            messages.info(request,"USERNAME DOES NOT EXISTS")
            return render(request,"user_login.html")

    return render(request, "user_login.html")

def admin_login(request):

    if request.method == "POST":
        username =  request.POST['username']
        password = request.POST['password']
        admin_login = authenticate(request, username = "admin@" + username, password = password)
        if admin_login is not None:
            login(request, admin_login)
            return redirect("admin_dashboard")
        else:
            messages.info(request,"USERNAME DOES NOT EXISTS")
            return render(request,"admin_login.html")

    return render(request, "admin_login.html")

@login_required(login_url="admin_login")
def admin_dashboard(request):    
    return render(request, "admin_dashboard.html")


@login_required(login_url="user_login")
def user_dashboard(request):

    get_user = Userregistration2.objects.get(username = request.user.username[9:])
    company_name = get_user.businessname
    return render(request, "user_dashboard.html",{"company_name":company_name})

@login_required(login_url="user_login")
def upload_signature(request):
    get_user = Userregistration2.objects.get(username = request.user.username[9:])
    company_name = get_user.businessname
    if Signature2.objects.filter(username = request.user.username[9:]).exists():

        get_sig = Signature2.objects.get(username = request.user.username[9:])
        si = get_sig.signature
        # si = si
        si = "../media/signature/"+request.user.username[9:]+".png"
    else:
        si = "../media/signature/blank.png"
    if request.method == "POST":

        check_exists = Signature2.objects.filter(username = request.user.username[9:])
        if len(check_exists) == 1:
            
            messages.info(request, "YOU CAN ONLY UPLOAD SIGNATURE ONCE ")
            return redirect("upload_signature")
        else:
            pass




        check_exists = Signature2.objects.filter(username = request.user.username[9:])
        if len(check_exists) == 1:
            check_exists.delete()
        username = request.user.username[9:]
     


        
        signature = request.FILES["signature"]
        user_signature = Signature2(username = username, signature = signature)
        user_signature.save()
        signature = str(signature)
        signature = signature.replace("(", "")
        signature = signature.replace(")", "")
        signature = signature.replace(" ", "_")
        get_key = Key.objects.get(username = "admin")
        key = get_key.key

        response = requests.post(
        'https://api.remove.bg/v1.0/removebg',
        files={'image_file': open('media/signature/'+str(signature), 'rb')},
        data={'size': 'auto'},
        headers={'X-Api-Key': key},

        # headers={'X-Api-Key': 'KL9nJ3q4ttu9aFFpZcEmWWrF'},
        # headers={'X-Api-Key': 'fEx2nV7xuEHTC9ED5Qx2mnFM'},

        )
        if response.status_code == requests.codes.ok:
        
            with open('media/signature/'+request.user.username[9:]+'.png', 'wb') as out:
                out.write(response.content)
                os.remove('media/signature/'+str(signature))    
                messages.info(request, "YOUR SIGNATURE IS UPLOADED")

                # old_signature = Signature2.objects.get(username = request.user.username[9:])
                # old_signature.delete()
                # new_signature = Signature2(username = request.user.username[9:], signature = 'signature/'+request.user.username[9:]+'.png')
                # new_signature.save()
                

                
                update_signature = Signature2.objects.get(username = request.user.username[9:])
                update_signature.signature = 'signature/'+request.user.username[9:]+'.png'
                update_signature.save()
        else:
            os.remove('media/signature/'+str(signature))
            err2 = response.text
            err2 = err2.find("code")
            err2 = response.text[err2+7:-4]
            messages.info(request, err2)
            print("Error:", response.status_code, response.text)
            
        return render(request, "upload_signature.html" , {"sig":si,"company_name":company_name})
    return render(request, "upload_signature.html", {"sig":si,"company_name":company_name})

@login_required(login_url="user_login")
def upload_logo(request):
    get_user = Userregistration2.objects.get(username = request.user.username[9:])
    company_name = get_user.businessname
    if Logo.objects.filter(username = request.user.username[9:]).exists():

        get_logo = Logo.objects.get(username = request.user.username[9:])
        logo = get_logo.logo
        logo = logo.url
        logo = "../media/businesslogo/"+request.user.username[9:]+".png"

        
    else:
        logo = "../media/businesslogo/blank.png"
    # check_date = Logo.objects.get(username = request.user.username[9:])
    # datey = check_date.datey
    # if datey > date.today():
    #     messages.info(request, "YOU NEED TO RE UPLOAD IN 30DAYS")
    #     return redirect("upload_logo")
    # else:
    #     pass
    if request.method == "POST":
        check_exists = Logo.objects.filter(username = request.user.username[9:])
        if len(check_exists) == 1:
            # check_exists.delete()
            check_date = Logo.objects.get(username = request.user.username[9:])
            datey = check_date.datey
            if datey > date.today():
                messages.info(request, "YOU CAN ONLY UPLOAD ONCE IN 30DAYS")
                return redirect("upload_logo")
            else:
                pass
        
        



        check_exists = Logo.objects.filter(username = request.user.username[9:])
        if len(check_exists) == 1:
            check_exists.delete()
        username = request.user.username[9:]
        logo = request.FILES["logo"]
        user_logo = Logo(username = username, logo = logo)
        user_logo.save()
        logo = str(logo)
        logo = logo.replace("(", "")
        logo = logo.replace(")", "")
        logo = logo.replace(" ", "_")
        get_key = Key.objects.get(username = "admin")
        key = get_key.key
        response = requests.post(
        'https://api.remove.bg/v1.0/removebg',
        files={'image_file': open('media/businesslogo/'+str(logo), 'rb')},
        data={'size': 'auto'},
        
        headers={'X-Api-Key': key},
        )
        if response.status_code == requests.codes.ok:
            with open('media/businesslogo/'+request.user.username[9:]+'.png', 'wb') as out:
                out.write(response.content)
                print("good")
                os.remove('media/businesslogo/'+str(logo))    
                messages.info(request, "YOUR LOGO IS UPLOADED")
                update_logo = Logo.objects.get(username = request.user.username[9:])
                update_logo.logo = 'businesslogo/'+request.user.username[9:]+'.png'
                update_logo.save()









        else:
            os.remove('media/signature/'+str(logo))
            err2 = response.text
            err2 = err2.find("code")
            err2 = response.text[err2+7:-4]
            messages.info(request, err2)
            print("Error:", response.status_code, response.text)
            set_date = Logo.objects.get(username = request.user.username[9:])
            set_date.datey = date.today()
            set_date.save()
        return render(request, "upload_logo.html",{"logo":logo,"company_name":company_name})
    return render(request, "upload_logo.html",{"logo":logo,"company_name":company_name})

@login_required(login_url="user_login")
def all_transaction(request):
    get_user = Userregistration2.objects.get(username = request.user.username[9:])
    company_name = get_user.businessname
    transaction = Transaction2.objects.filter(username = request.user.username[9:])
    return render(request, "all_transaction.html",{"transaction":transaction,"company_name":company_name})

@login_required(login_url="admin_login")
def all_transactions(request):

    
    transaction = Transaction2.objects.all()
    return render(request, "all_user_transaction.html",{"transaction":transaction})

@login_required(login_url="admin_login")
def all_user(request):
    
    user = Userregistration2.objects.all()
    return render(request, "all_user.html",{"user":user})

@login_required(login_url="admin_login")
def admin_query_user(request,search):
    search = search
    if search == "all":
        user = Userregistration2.objects.all()
        return render(request, "all_user.html",{"user":user,"len": len(user)})
    else:
        user = Userregistration2.objects.filter(username = search)
        return render(request, "admin_query_user.html",{"user":user,"len": len(user)})

@login_required(login_url="admin_login")
def admin_query_user1(request):
    search = request.POST['search']
    if len(search) == 0:
        search = "all"
    return redirect("admin_query_user/"+search)


@login_required(login_url="user_login")
def query_transaction(request,search):
    get_user = Userregistration2.objects.get(username = request.user.username[9:])
    company_name = get_user.businessname
    
    search = search

    if search == "all":
        transaction = Transaction2.objects.filter(username = request.user.username[9:])
        return render(request, "query_transaction.html",{"transaction":transaction,"len": len(transaction)})
    else:
        transaction = Transaction2.objects.filter(username = request.user.username[9:], receiver_name__icontains = search)
        return render(request, "query_transaction.html",{"transaction":transaction,"len": len(transaction),"company_name":company_name})

@login_required(login_url="user_login")
def query_transaction1(request):
    
    
    search = request.POST['search']
    if len(search) == 0:
        search = "all"
    return redirect("query_transaction/"+search)


@login_required(login_url="admin_login")
def admin_query_transaction(request,search):
    search = search
    if search == "all":
        transaction = Transaction2.objects.all()
        return render(request, "admin_query_transaction.html",{"transaction":transaction,"len": len(transaction)})
    else:
        transaction = Transaction2.objects.filter(username = search)
        return render(request, "admin_query_transaction.html",{"transaction":transaction,"len": len(transaction)})

@login_required(login_url="admin_login")
def admin_query_transaction1(request):
    
    search = request.POST['search']
    if len(search) == 0:
        search = "all"
    return redirect("admin_query_transaction/"+search)




@login_required(login_url="user_login")
def delete_receipt(request,id):
    transaction = Transaction2.objects.get(id = id)
    transaction.delete()
    return redirect("all_transaction")

@login_required(login_url="admin_login")
def delete_receipt(request,id):
    transaction = Transaction2.objects.get(id = id)
    transaction.delete()
    return redirect("all_transaction")

@login_required(login_url="admin_login")
def admin_delete_receipt(request,id):
    transaction = Transaction2.objects.get(id = id)
    transaction.delete()
    return redirect("all_transactions")


@login_required(login_url="user_login")
def query_receipt(request,id):

    get_user = Userregistration2.objects.get(username = request.user.username[9:])
    company_name = get_user.businessname
    if Transaction2.objects.filter(id = id, username = request.user.username[9:]).exists():
        
        receipt_id = id
        transaction = Transaction2.objects.get(id = receipt_id)
        date = transaction.date
        receiver = transaction.receiver_name
        amount_naira = transaction.amount_in_word_naira
        description = transaction.description
        digit_naira = transaction.amount_in_digit_naira
        username = request.user.username[9:]
        get_user = Userregistration2.objects.get(username = username)
        company_name = get_user.businessname 
        company_address = get_user.businessaddress 
        get_logo = Logo.objects.get(username = username)
        # company_logo = get_logo.logo
        company_logo = "../../media/businesslogo/"+request.user.username[9:]+".png"

        get_signature = Signature2.objects.get(username = username)
        signature = "../../media/signature/"+request.user.username[9:]+".png"
        context = {
                "receiver":receiver,
                "amount_naira":amount_naira,
                "description":description,
                "digit_naira":digit_naira,
                "company_name":company_name,
                "company_address":company_address,
                "company_logo":company_logo,
                "signature":signature,
                "date":date,
                "id":transaction.id,
                "company_name":company_name
                

            }
        get_user = Userregistration2.objects.get(username = request.user.username[9:])
        receipt = get_user.receipt_type
        return render(request, receipt+".html",context)

        # return render(request, "query_receipt.html",context)
    else:
        return render(request, "error_receipt.html",{"company_name":company_name})


@login_required(login_url="admin_login")
def admin_query_receipt(request,id,username):

    
    if Transaction2.objects.filter(id = id).exists():
        
        receipt_id = id
        transaction = Transaction2.objects.get(id = receipt_id)
        date = transaction.date
        receiver = transaction.receiver_name
        amount_naira = transaction.amount_in_word_naira
        description = transaction.description
        digit_naira = transaction.amount_in_digit_naira
        get_user = Userregistration2.objects.get(username = username)
        company_name = get_user.businessname 
        company_address = get_user.businessaddress 
        get_logo = Logo.objects.get(username = username)
        # company_logo = get_logo.logo
        company_logo = "../../../media/businesslogo/"+username+".png"

        get_signature = Signature2.objects.get(username = username)
        # signature = get_signature.signature
        signature = "../../../media/signature/"+username+".png"

        context = {
                "receiver":receiver,
                "amount_naira":amount_naira,
                "description":description,
                "digit_naira":digit_naira,
                "company_name":company_name,
                "company_address":company_address,
                "company_logo":company_logo,
                "signature":signature,
                "date":date,
                "id":transaction.id,
                "company_name":company_name
                

            }
        return render(request, "admin_query_receipt.html",context)
    else:
        return render(request, "error_receipt.html",{"company_name":company_name})



@login_required(login_url="user_login")
def plot(request):
    get_user = Userregistration2.objects.get(username = request.user.username[9:])
    company_name = get_user.businessname
    if request.method == "POST":
        date1 = request.POST["date1"]
        date2 = request.POST['date2']

            
        new = date1.split("-")
            
        s1 = int(new[0])
        s2 = new[1]
        s3 = new[2]

        if s2[0] == "0":
            s2 = s2[1:]
        if s3[0] == "0":
            s3 = s3[1:]

        s1 = int(s1)
        s2 = int(s2)
        s3 = int(s3)

        new2 = date2.split("-")
        e1 = new2[0]
        e2 = new2[1]
        e3 = new2[2]
        if e2[0] == "0":
            e2 = e2[1:]
        if e3[0] == "0":
            e3 = e3[1:]

        e1 = int(e1)
        e2 = int(e2)
        e3 = int(e3)

        start = date(s1, s2, s3)
        end = date(e1, e2, e3)
        delta = timedelta(days=1)
        dates = []
        real = []
        unit_per_date = []
        while start <= end:
            dates.append(start.isoformat())
            start += delta
        
        for x in dates:
            if Transaction2.objects.filter(date = x, username = request.user.username[9:]).exists():
                real.append(x)
        for y in real:
            query = Transaction2.objects.filter(date = y, username = request.user.username[9:])
            unit_per_date.append(len(query))
            
            

        context = {
        "real_date":real,
        "date":date1,
        "new":new,
        "s1":s1,
        "s2":s2,
        "s3":s3,
        "dates":dates,
        "amount":unit_per_date,
        "company_name":company_name
            
        }


        if request.POST["report_type"] == "graph":
            font1 = {'family':'serif','color':'blue','size':20}
            font2 = {'family':'serif','color':'darkred','size':15}
            plt.title("Sales Report", fontdict = font1)
            plt.xlabel("Dates", fontdict = font2)
            plt.ylabel("Number of Sales", fontdict = font2)
            plt.plot(real, unit_per_date)
            plt.show()
            return render(request, "plot.html",{"company_name":company_name})
        elif request.POST["report_type"] == "bar":
            font1 = {'family':'serif','color':'blue','size':20}
            font2 = {'family':'serif','color':'darkred','size':15}
            plt.title("Sales Report", fontdict = font1)
            plt.xlabel("Dates", fontdict = font2)
            plt.ylabel("Number of Sales", fontdict = font2)    
            plt.bar(real, unit_per_date)
            plt.show()
            return render(request, "plot.html",{"company_name":company_name})
        elif request.POST["report_type"] == "pie":
            mylabels = real
            font1 = {'family':'serif','color':'blue','size':20}
            font2 = {'family':'serif','color':'darkred','size':15}
            plt.title("Sales Report", fontdict = font1)
            
                
            y = unit_per_date
            plt.pie(y, labels = mylabels,  shadow = True)
            plt.legend(title = "Dates:" )
            plt.show() 
            return render(request, "plot.html",{"company_name":company_name})
        else:
            a ={}
            for x in range(0,len(real)):
                    
                a[real[x]] = unit_per_date[x]

            v = []
            for x,y in a.items():
                v.append(x)
                    
            return render(request, "sales_table.html",{"date":real,"amount":unit_per_date,"a":a,"v":v,"company_name":company_name})

            return render(request, "plot.html",context)
        
    return render(request, "plot.html",{"company_name":company_name})


@login_required(login_url="user_login")
def update_profile(request):



    get_user = Userregistration2.objects.get(username = request.user.username[9:])
    company_name = get_user.businessname
    company_address = get_user.businessaddress

    
    context = {
        "company_name":company_name,
        "company_address": company_address
    }

    if request.method == "POST":
        # new_name = request.POST["business_name"]
        new_address = request.POST["business_address"]

        get_user = Userregistration2.objects.get(username = request.user.username[9:])
        # get_user.businessname = new_name
        get_user.businessaddress = new_address
        get_user.save()
        context = {
        # "company_name":new_name,
        "company_address": new_address
        }
        messages.info(request, "Profile Update Successfully")
        return render(request,"update_profile.html",context)

    return render(request, "update_profile.html",context)


def logout(request):
    auth.logout(request)
    return redirect("user_login")

def admin_logout(request):
    auth.logout(request)
    return redirect("admin_login")

@login_required(login_url="admin_login")
def key(request):
    get_key = Key.objects.get(username = "admin")
    context = {
                "key":get_key.key
            }
    if request.method == "POST":
        
        key = request.POST['key']
        get_key = Key.objects.get(username = "admin")
        get_key.key = key
        get_key.save()

        
        return redirect("key")
    return render(request,"key.html",context)

@login_required(login_url="user_login")
def change_password(request):
    if request.method == "POST":
        old_password = request.POST['old_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']
        check = Userregistration2.objects.get(username = request.user.username[9:])
        password = check.password

        if password == old_password:
            if new_password == confirm_password:
                check.password = new_password
                messages.info(request, "Password Changed Successfully")
                return redirect("change_password")
            else:
                messages.info(request, "New Password and confirm Password Did not Match")
                return redirect("change_password")
        else:
            messages.info(request, "Old Password Incorrect")

        return redirect("change_password")
    return render(request, "change_password.html")

def forgotten_password(request):

    if request.method == "POST":
        email = request.POST['email']
        if Userregistration2.objects.filter(email = email).exists():
            check_exists = Tmpforgetpassword.objects.filter(email = email)
            if len(check_exists) == 1:
                check_exists.delete()
            characters = list(string.digits)
            random.shuffle(characters)

            code = []

            for x in range(6):
                code.append(random.choice(characters))
            random.shuffle(code)

            code = "".join(code)
            tmp_reg = Tmpforgetpassword(email = email, code = code)
            tmp_reg.save()

            
            
            
            
            sender = "adebimpeazeezniyi@gmail.com"
            receiver = email
            body = "Your Verification Code is " + code
            subject = "Email Verification"
            password = 'hizcbuuvzjsreojr'


            em = EmailMessage()
            em["From"] = sender
            em["To"] = receiver
            em["subject"] = subject
            em.set_content(body)

            context = ssl.create_default_context()

            with smtplib.SMTP_SSL("smtp.gmail.com",465,context=context) as smtp:
                smtp.login(sender,password)
                smtp.sendmail(sender,receiver,em.as_string())
            return redirect("verify_forgotten_password/"+email)
        else:
            messages.info(request, "No Such User Exist")
            return redirect("forgotten_password")
    return render(request, "forgotten_password.html")

def verify_forgotten_password(request,id):
    if request.method == "POST":
        code = request.POST['code']
        
        tmp_reg = Tmpforgetpassword.objects.get(email = id)
        dbcode = tmp_reg.code

        if code == dbcode:
            status = Tmpforgetpassword.objects.get(email = id)
            status.status = 1
            status.save()
            return redirect("../change_password2/"+id)

        else:
            messages.info(request, "Invalid Activation Code")
            return redirect("../verify_forgotten_password/"+id)

    return render(request, "verify_email.html")

def change_password2(request,id):

    if request.method == "POST":
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']
        
        check = Tmpforgetpassword.objects.filter(email = id)
        status = Tmpforgetpassword.objects.get(email = id)
        if status.status == "0":

            messages.info(request, "Not Permitted")
            return redirect("forgotten_password")
        if len(check) == 0:
            messages.info(request, "Not Permitted")
            return redirect("forgotten_password")
       
        
            
        else:
            if new_password == confirm_password:
                check = Tmpforgetpassword.objects.filter(email = id)
                check.delete()

                # status = Tmpforgetpassword.objects.get(email = id)
                # status.status = 0
                # status.save()
                user = Userregistration2.objects.get(email = id)
                user.password = new_password
                user.save()
                messages.info(request, "Password has been reset")
                return redirect("user_login")
            else:
                messages.info(request, "Both Password did not match")
                return redirect("../change_password2/"+id)
    return render(request, "change_password2.html")


def change_receipt(request):
    if request.method == "POST":
        receipt = request.POST['receipt']
        get_user = Userregistration2.objects.get(username = request.user.username[9:])
        get_user.receipt_type = receipt
        get_user.save()
        messages.info(request, "Template Changed Successfully")
    return render(request, "change_receipt.html")


def admin_delete_user(request,id):
    get_user = Userregistration2.objects.get(id = id)
    get_user.delete()
    return redirect("all_user")

def index2(request):
    return render(request, "index2.html")


    # if request.method == "POST":
    #     get_key = key.objects.all()
    #     context = {
    #         "key":get_key
    #     }
    #     return render(request,"key.html",context)

    # return render(request,"key.html")






    # plt.plot([1,2,3,4],[2,1,4,5],"y+")
    # plt.ylabel("Some Numbers")
    # plt.show()

    # names = ['group_a', 'group_b', 'group_c']
    # values = [1, 10, 100]

    # plt.figure(figsize=(9, 3))

    # plt.subplot(131)
    # plt.bar(names, values)
    # plt.subplot(132)
    # plt.scatter(names, values)
    # plt.subplot(133)

    # plt.plot(names, values)
    # plt.suptitle('Categorical Plotting')
    # plt.show()


    # plt.figure(1)                # the first figure
    # plt.subplot(211)             # the first subplot in the first figure
    # plt.plot([1, 2, 3])
    # plt.subplot(212)             # the second subplot in the first figure
    # plt.plot([4, 5, 6])


    # plt.figure(2)                # a second figure
    # plt.plot([4, 5, 6])          # creates a subplot() by default

    # plt.figure(1)                # first figure current;
    #                          # subplot(212) still current
    # plt.subplot(211)             # make subplot(211) in the first figure
    #                          # current
    # plt.title('Easy as 1, 2, 3') # subplot 211 title
    # plt.show()


#     mu, sigma = 100, 15
#     x = mu + sigma * np.random.randn(10000)

# # the histogram of the data
#     n, bins, patches = plt.hist(x, 50, density=True, facecolor='g', alpha=0.75)


#     plt.xlabel('Smarts')
#     plt.ylabel('Probability')
#     plt.title('Histogram of IQ')
#     plt.text(60, .025, r'$\mu=100,\ \sigma=15$')
#     plt.axis([40, 160, 0, 0.03])

#     plt.grid(True)
#     plt.show()



