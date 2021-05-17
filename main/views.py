from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import *
from django.contrib import messages
import uuid
from django.conf import settings
from django.core.mail import send_mail
from django.contrib import auth
from django.contrib.auth.decorators import login_required


# Create your views here.

def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        if not User.objects.filter(username=username).exists():
            messages.error(request, "User Not found")
            return redirect("/")
        user = User.objects.get(username=username)
        detail = Detail.objects.get(user=user)
        if not detail.is_verified:
            messages.error(request, "User not verified,please check your mail")
            return redirect("/")
        user = auth.authenticate(username=username, password=password)
        if user is None:
            messages.error(request, "Incorrect Password")
            return redirect("/")
        auth.login(request, user)
        return redirect("home")
    return render(request, "login.html")


@login_required
def home(request):
    return render(request, "home.html")

def logout(request):
    auth.logout(request)
    return redirect("login")

def verify(request, token):
    detail = Detail.objects.get(token=token)
    if detail:
        if detail.is_verified:
            messages.info(request, "Your account is already verified")
            return redirect("/")
        detail.is_verified = True
        detail.save()
        messages.info(request, "Your account has been verified")
        return redirect("/")
    else:
        return redirect("error")


def error(request):
    return render(request, "error.html")


def send_mail_after_signUp(email, token):
    subject = "This is verification mail"
    message = f"Hi, click this is link to verify http://127.0.0.1:8000/verify/{token} "
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)


def signUp(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username Already Exist")
            return redirect("signUp")
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email Already Exist")
            return redirect("signUp")
        user = User.objects.create_user(username=username, email=email, password=request.POST['password'])
        token = str(uuid.uuid4())
        detail = Detail(user=user, token=token)
        detail.save()
        messages.success(request, "verification mail has been sent to your mail. Please verify It.")
        send_mail_after_signUp(email, token)
        return redirect("signUp")
    return render(request, "signUp.html")
