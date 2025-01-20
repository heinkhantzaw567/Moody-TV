from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
# Create your views here.
from .models import User
from django.db import IntegrityError
from openai import OpenAI
import requests
def index(request):
    
   
    return render(request, 'chat/index.html')

def signup_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        print(confirmation)
        if password != confirmation:
            return render(request, 'chat/signup.html', {
                "message": "Passwords must match."
            })
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, 'chat/signup.html', {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("chat:home"))
    else:
        return render(request, 'chat/signup.html')
   
   

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("chat:home"))
        else:
            return render(request, "chat/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "chat/login.html")



def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("auctions:index"))

def home(request):
    
    if request.user.is_authenticated:
        if request.method == "POST":
            # mood = request.POST["mood"]
            # genre = request.POST["genre"]
            # reason = request.POST["reason"]
            # emotion = request.POST["emotion"]
            return render(request, 'chat/home.html')
        else:
            return render(request, 'chat/home.html')
    else:
        return HttpResponseRedirect(reverse("chat:login"))
    
def display(request):
    context = {
        'show_main': False,  # Set this to False when you want to display the div instead
    }
    return render(request, 'chat/display.html',
                  context)