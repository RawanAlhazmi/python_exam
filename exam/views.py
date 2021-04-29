from django.shortcuts import render,redirect
from .models import User,Wish
from django.contrib import messages
import bcrypt
from datetime import date, datetime, timedelta

def index(request):
    if 'uid' in request.session:
        return redirect('/wishes')
    return render(request,"reg_login.html")

######### Registration & Login Section #########

def register(request):
    if request.method == "POST":
        errors = User.objects.basic_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        hash_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        new_user = User.objects.create(
                first_name = request.POST['f_name'],
                last_name = request.POST['l_name'],
                email = request.POST['email'],
                password = hash_pw
            )
        request.session['uid'] = new_user.id
    return redirect("/wishes")

def login(request):
    if request.method == "POST":
        errors = User.objects.login_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        user = User.objects.filter(email=request.POST['email']) # why are we using filter here instead of get?
        if user: 
            logged_user = user[0]  
            if  bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
                request.session['uid'] = logged_user.id
                return redirect('/wishes')
    return redirect("/")

def wishes(request):
    if 'uid' not in request.session:
        return redirect("/")
    user_id = request.session['uid']
    context = {
        "user": User.objects.get(id=user_id),
        "wishes": Wish.objects.all().order_by("-id"),
        "g_wishes": Wish.objects.all()
    }
    return render(request,"wishes.html",context)

def new_wish(request):
    if 'uid' not in request.session:
        return redirect("/")
    context = {
        "user": User.objects.get(id=request.session['uid']),
    }
    return render(request,"new_wish.html",context)

def stats_wish(request):
    if 'uid' not in request.session:
        return redirect("/")
    user = User.objects.get(id=request.session['uid'])
    context = {
        "user": User.objects.get(id=request.session['uid']),
        "wishes": Wish.objects.all(),
        "g_wishes": Wish.objects.filter(granted=True),
        "user_g": user.wishes.filter(granted=True),
        "user_p": user.wishes.filter(granted=False),
    }
    return render(request,"stats_wish.html",context)

def create_wish(request):
    if request.method == "POST":
        errors = Wish.objects.basic_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect("/wishes/new")
        Wish.objects.create(
            Item=request.POST['item'],
            description=request.POST['desc'],
            wisher=User.objects.get(id=request.session['uid'])
        )
    return redirect("/wishes")

def update_wish(request,w_id):
    if request.method == "POST":
        errors = Wish.objects.basic_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect(f"/wishes/edit/{w_id}")
        wish = Wish.objects.get(id=w_id)
        wish.Item = request.POST['item']
        wish.description = request.POST['desc']
        wish.save()
        return redirect("/wishes")

def granted_wish(request,w_id):
    wish=Wish.objects.get(id=w_id)
    wish.granted = True
    wish.granted_date = datetime.now()
    wish.save()
    return redirect("/wishes")

def delete_wish(request,w_id):
    wish=Wish.objects.get(id=w_id)
    wish.delete() 
    return redirect("/wishes")

def edit_wish(request,w_id):
    if 'uid' not in request.session:
        return redirect("/")
    context = {
        "user": User.objects.get(id=request.session['uid']),
        "wish": Wish.objects.get(id=w_id)
    }
    return render(request,"edit_wish.html",context)

def like_wish(request,w_id):
    user = User.objects.get(id=request.session['uid'])
    wish = Wish.objects.get(id=w_id)
    wish.liked_by.add(user)
    return redirect("/wishes")

def destroy(request):
    del request.session['uid']
    return redirect('/')