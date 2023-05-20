from django.db import models
from django.contrib.auth import get_user_model
import datetime
from datetime import date,timedelta

User = get_user_model()



class Transaction2(models.Model):
    receiver_name = models.CharField(max_length=200)
    amount_in_word_naira = models.CharField(max_length=200)
    amount_in_word_kobo = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    description2 = models.CharField(max_length=200)
    amount_in_digit_naira = models.CharField(max_length=200)
    amount_in_digit_kobo = models.CharField(max_length=200)
    username = models.CharField(max_length=200)
    date = models.DateField()
    # date = models.DateField(default=datetime.date.today())
  
    def __str__(self):
        return self.receiver_name



class Userregistration2(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    businessname = models.CharField(max_length=200)
    businessaddress = models.CharField(max_length=200, default = "Your Address Here")
    email = models.CharField(default=username, max_length=200)
    receipt_type = models.CharField(default="receipt1", max_length=200)

    
    def __str__(self):
        return self.businessname

class Logo(models.Model):
    username = models.CharField(max_length=200)
    logo = models.FileField(upload_to="businesslogo")
    datey = models.DateField(default=date.today() + timedelta(days=30))
    def __str__(self):
        return self.username




class Signature2(models.Model):
    username = models.CharField(max_length=200)
    signature = models.FileField(upload_to="signature")

    def __str__(self):
        return self.username

class Key(models.Model):
    username = models.CharField(max_length=200, default="admin")
    key = models.CharField(max_length=200)

    def __str__(self):
        return self.key



class Tmpreg(models.Model):
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    businessname = models.CharField(max_length=200)
    businessaddress = models.CharField(max_length=200, default = "Your Address Here")
    email = models.CharField(max_length=200)
    code = models.CharField(max_length=200)
    
    def __str__(self):
        return self.username 

class Tmpforgetpassword(models.Model):
    email = models.CharField(max_length=200)
    status = models.CharField(max_length=200, default=0)

    code = models.CharField(max_length=200)

    def __str__(self):
        return self.code 