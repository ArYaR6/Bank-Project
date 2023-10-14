from django.shortcuts import render, redirect

from django.http import HttpResponse
from .forms import *
from .models import *
import os
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from django.shortcuts import render, redirect
from django.core.mail import send_mail


# Create your views here.
def index(request):
    return render(request, 'index.html')


def regform(request):
    return render(request, 'regform.html')


def index1(request):
    return render(request, 'index1.html')


def bankview(request):
    if request.method == 'POST':
        a = bankform(request.POST, request.FILES)
        if a.is_valid():
            fn = a.cleaned_data['fname']
            ln = a.cleaned_data['lname']
            un = a.cleaned_data['uname']
            em = a.cleaned_data['email']
            ph = a.cleaned_data['phone']
            ac = "15" + str(ph)

            file = a.cleaned_data['file']
            pi = a.cleaned_data['pin']
            pis = a.cleaned_data['pins']

            if pi == pis:
                b = bankmodel(fname=fn, lname=ln, uname=un, email=em, phone=ph, file=file, pin=pi, balance=0,
                              acnum=int(ac))
                b.save()

                subject = "Yoyr account has been created"
                message = f"Your new account number is {ac}"
                email_from = "jojin3k@gmail.com"
                email_to = em
                send_mail(subject, message, email_from, [email_to])

                return redirect(logview)
            else:
                return HttpResponse("password is incorrect")
        else:
            return HttpResponse("Registration is Failed")

    return render(request, 'regform.html')


def logview(request):
    if request.method == 'POST':
        a = logform(request.POST)
        if a.is_valid():
            em = a.cleaned_data['uname']
            ps = a.cleaned_data['pin']
            b = bankmodel.objects.all()
            for i in b:  # name=ggh,email=hhjjj,psw=5555)
                if i.uname == em and i.pin == ps:
                    request.session['id'] = i.id
                    return redirect(prview)
            else:
                return HttpResponse("Login Failed!!")

    return render(request, 'index.html')


def prview(request):
    try:
        id1 = request.session['id']
        a = bankmodel.objects.get(id=id1)
        img = str(a.file).split('/')[-1]
        return render(request, 'profile.html', {'a': a, 'img': img})
    except:
        return redirect(logview)


def pdetail(request, id):
    return render(request, 'editprofile.html')


def editdata(request):
    id1 = request.session['id']
    a = bankmodel.objects.get(id=id1)
    if request.method == 'POST':
        a.fname = request.POST.get('fname')
        a.lname = request.POST.get('lname')
        a.phone = request.POST.get('phone')
        a.email = request.POST.get('email')

        a.save()
        return redirect(prview)
    return render(request, 'editprofile.html', {'a': a})


def picedit(request):
    id1 = request.session['id']
    a = bankmodel.objects.get(id=id1)
    img = str(a.file).split('/')[-1]
    if request.method == 'POST':
        a.uname = request.POST.get('uname')
        # image#
        if len(request.FILES) != 0:
            if len(a.file) > 0:
                os.remove(a.file.path)
            a.file = request.FILES['file']
        a.save()
        return redirect(prview)

    return render(request, 'editpic.html', {'a': a, 'img': img})


def addmoney(request):
    id1 = request.session['id']
    x = bankmodel.objects.get(id=id1)
    if request.method == 'POST':
        am = request.POST.get('amount')
        request.session['am'] = am
        request.session['acnum'] = x.acnum

        x.balance += int(am)
        x.save()
        b = addamount(amount=am, uid=request.session['id'])
        b.save()
        pin = request.POST.get('pi')
        if int(pin) == x.pin:
            return redirect(su)
        else:
            return HttpResponse("FAIL")
    return render(request, 'addamount.html')


def su(request):
    am = request.session['am']
    acc = request.session['acnum']

    return render(request, 'success.html', {'am': am, 'acnum': acc})


def withdraw(request):
    id1 = request.session['id']
    x = bankmodel.objects.get(id=id1)
    if request.method == 'POST':
        am = request.POST.get('amount')
        request.session['am'] = am
        request.session['acnum'] = x.acnum
        if (x.balance >= int(am)):
            x.balance -= int(am)
            x.save()
            b = withdrawamount(amount=am, uid=request.session['id'])
            b.save()
            pin = request.POST.get('pi')
            if int(pin) == int(x.pin):

                return redirect(wsu)
            else:
                return HttpResponse("Withdraw Failed")
        else:
            return HttpResponse("Insufficient Balance")

    return render(request, 'withdraw.html')


def wsu(request):
    am = request.session['am']
    acc = request.session['acnum']
    return render(request, 'wisu.html', {'am': am, 'acnum': acc})


def checkbalance(request):
    id1 = request.session['id']
    x = bankmodel.objects.get(id=id1)
    if request.method == 'POST':
        request.session['balance'] = x.balance
        request.session['acnum'] = x.acnum

        pin = request.POST.get('pin')
        if int(pin) == x.pin:
            return redirect(cubalance)
        else:
            return HttpResponse("FAIL")
    return render(request, 'checkbalance.html')


def cubalance(request):
    bc = request.session['balance']
    acc = request.session['acnum']

    return render(request, 'currentbalance.html', {'balance': bc, 'acnum': acc})


def mini(request):
    id1 = request.session['id']
    x = bankmodel.objects.get(id=id1)
    pin = request.POST.get('pin')
    if request.method == 'POST':
        if int(pin) == int(x.pin):
            a = request.POST.get('ministatement')
            if a == 'deposit':
                return redirect(deposit)
            elif a == 'withdraw':
                return redirect(mwithdraw)
        else:
            return HttpResponse("PIN ERROR")
    return render(request, 'ministatement.html')


def deposit(request):
    x = addamount.objects.all()
    id = request.session['id']
    return render(request, 'deposit.html', {'x': x, 'id': id})


def mwithdraw(request):
    x = withdrawamount.objects.all()
    id = request.session['id']
    return render(request, 'miniwithdraw.html', {'x': x, 'id': id})


def news(request):
    if request.method == 'POST':
        a = nform(request.POST)
        if a.is_valid():
            ti = a.cleaned_data['topic']
            co = a.cleaned_data['content']

            b = newmodels(topic=ti, content=co)
            b.save()

            return redirect(newsdisplay)
        else:
            return HttpResponse("data is not added")
    return render(request, 'new.html')


def newsdisplay(request):
    x = newmodels.objects.all()
    id1 = []
    tp = []
    co = []
    dt = []
    for i in x:
        id = i.id
        id1.append(id)
        top = i.topic
        tp.append(top)
        con = i.content
        co.append(con)
        dat = i.date
        dt.append(dat)
    pair = zip(tp, co, dt, id1)

    return render(request, 'ndis.html', {'x': pair})


def adminlo(request):
    if request.method == 'POST':
        a = adminform(request.POST)
        if a.is_valid():

            username = a.cleaned_data['username']
            password = a.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                return redirect(adminpro)
            else:
                return HttpResponse("FAILED")
    return render(request, 'loadmin.html')


def adminpro(request):
    return render(request, 'adminpro.html')

def admindisplay(request):
    x = newmodels.objects.all()
    id1=[]
    tp=[]
    co=[]
    dt=[]
    for i in x:
        id = i.id
        id1.append(id)
        top=i.topic
        tp.append(top)
        con=i.content
        co.append(con)
        dat=i.date
        dt.append(dat)
    pair=zip(tp,co,dt,id1)

    return render(request, 'admindisplay.html', {'x':pair})

def nedit(request,id):

    a = newmodels.objects.get(id=id)
    if request.method == 'POST':
        a.topic = request.POST.get('topic')
        a.content = request.POST.get('content')

        a.save()
        return redirect(admindisplay)
    return render(request, 'editnews.html', {'a': a})

def ndelete(request, id):
    a = newmodels.objects.get(id=id)
    # os.remove(a.) #it is used to remove path of file frm static
    a.delete()
    return redirect(admindisplay)

def ndis(request):
    return render(request,'ndis.html')

def wish(request,id):
    a=newmodels.objects.get(id=id)
    a1=wishlist.objects.all()
    for i in a1:
        if i.newsid==a.id and i.uid==request.session['id']:
            return HttpResponse('item already in wishlist')
    
    b=wishlist(topic=a.topic,content=a.content,date=a.date,newsid=a.id,uid=request.session['id'])
    b.save()
    return redirect(wldisplay)

def wldisplay(request):
    x = wishlist.objects.all()
    id = request.session['id']
    return render(request, 'wlist.html', {'x':x,'id':id})

from django.contrib.auth import logout
def logout_view(request):
    logout(request)
    return redirect(logview)

def bus(request):
    return render(request,'business.html')

def priority(request):
    return render(request,'priority.html')

def forgot_password(request):
    a=bankmodel.objects.all()
    if request.method=='POST':
        em=request.POST.get('email')
        ac=request.POST.get('acnum')
        for i in a:
            if (i.email==em and i.acnum==int(ac)):
                id=i.id
                subject='password change'
                message=f"http://127.0.0.1:8000/bank_app/change_password/{id}"
                frm='jojin3k@gmail.com'
                to=em
                send_mail(subject,message,frm,[to])
                return HttpResponse('check email')
        else:
            return HttpResponse('sorry')
    return render(request,'forgot.html')

def change_password(request,id):
    a=bankmodel.objects.get(id=id)
    if request.method=="POST":
        p1=request.POST.get('pin')
        p2=request.POST.get('repin')
        if p1==p2:
            a.pin=p1
            a.save()
            return HttpResponse('password changed')
        else:
            return HttpResponse('sorry')
    return render(request,'change.html')

def indexs(request):
    return render(request,'index1.html')


