from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.conf  import settings

from .models import *

# Create your views here.

def index(request):
    return render(request, "transit/index.html")

@login_required
def dashboard(request):
    transits = Transit.objects.all()
    transits = [i.name for i in transits]

    if request.method == "POST":
        start = request.POST["start"]
        destination = request.POST["destination"]
        return render(request, "transit/dashboard.html", {
            "transits": transits
        })
    else:
        return render(request, "transit/dashboard.html", {
            "transits": transits
        })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("dashboard"))
        else:
            return render(request, "transit/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "transit/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("login"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        latitude = request.POST["lat"]
        longitude = request.POST["long"]
        if password != confirmation:
            return render(request, "transit/register.html", {
                "message": "Passwords must match."
            })
        new_location = Location(latitude=latitude, longitude=longitude)
        new_location.save()
        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.location = new_location
            user.save()
        except IntegrityError:
            return render(request, "transit/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("dashboard"))
    else:
        return render(request, "transit/register.html")


def custom_404(request):
    return render(request, "transit/404.html", status=404)