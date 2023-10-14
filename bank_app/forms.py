from django import forms

class bankform(forms.Form):
    fname=forms.CharField(max_length=50)
    lname=forms.CharField(max_length=50)
    uname=forms.CharField(max_length=50)
    email=forms.EmailField()
    phone=forms.IntegerField()
    file=forms.FileField()
    pin=forms.IntegerField()
    pins=forms.IntegerField()

class logform(forms.Form):
    uname=forms.CharField(max_length=50)
    pin=forms.IntegerField()

class nform(forms.Form):
    topic=forms.CharField(max_length=50)
    content=forms.CharField(max_length=500)

class adminform(forms.Form):
    password=forms.CharField(max_length=20)
    username=forms.CharField(max_length=20)
