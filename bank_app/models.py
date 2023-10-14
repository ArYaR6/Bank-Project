from django.contrib.auth.models import User
from django.db import models
from django.forms import ModelForm


# Create your models here.

class bankmodel(models.Model):
    fname=models.CharField(max_length=50)
    lname=models.CharField(max_length=50)
    uname=models.CharField(max_length=50)
    email=models.EmailField()
    phone=models.IntegerField()
    file=models.FileField(upload_to='bank_app/static')
    pin=models.IntegerField()
    balance=models.IntegerField()
    acnum=models.IntegerField()
    def __str__(self):
        return self.fname

class addamount(models.Model):
    uid=models.IntegerField()
    amount=models.IntegerField()
    date=models.DateField(auto_now_add=True)
    def __int__(self):
        return self.date

class withdrawamount(models.Model):
    uid = models.IntegerField()
    amount=models.IntegerField()
    date=models.DateField(auto_now_add=True)

# class minimodel(models.Model):
#     choice=[
#         ('Deposit','Deposit'),
#         ('Withdraw','Withdraw')
#       ]
#     pin=models.IntegerField()
#
#     MiniStatement=models.IntegerField(choices=choice) #checktbox




class newmodels(models.Model):
    topic=models.CharField(max_length=500)
    content=models.CharField(max_length=2000)
    date=models.DateField(auto_now_add=True)

class wishlist(models.Model):
    uid = models.IntegerField()
    newsid=models.IntegerField()
    topic = models.CharField(max_length=500)
    content = models.CharField(max_length=2000)
    date = models.DateField()
    def __int__(self):
        return self.date
