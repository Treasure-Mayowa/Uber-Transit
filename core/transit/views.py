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
import requests
from math import radians, sin, cos, sqrt, atan2

# Create your views here.

def index(request):
    if request.user.is_authenticated: 
        if Driver.objects.get(user=request.user).user.username != "":
            return render(request, "transit/index.html", {
                "driver": True
            })
    else:
        return render(request, "transit/index.html")

@login_required
def dashboard(request):
    transits = Transit.objects.all()
    transits = [i.name for i in transits]
    api_key = settings.MAP_API_KEY
    
    if request.method == "POST":
        start = request.POST["start"]
        destination = request.POST["destination"]
        
        response = requests.get(f"https://graphhopper.com/api/1/geocode?q={start}&locale=en&key={api_key}")
        data = response.json()

        res = requests.get(f"https://graphhopper.com/api/1/geocode?q={destination}&locale=en&key={api_key}")
        res = res.json()

        close_transits = journey(data["hits"][0]["point"]["lat"], data["hits"][0]["point"]["lng"], res["hits"][0]["point"]["lat"], res["hits"][0]["point"]["lng"])
        close_transits = [transit.name for transit in close_transits]

        return render(request, "transit/dashboard.html", {
            "transits": transits, "close_transits": close_transits, "results": True
        })
    else:
        return render(request, "transit/dashboard.html", {
            "transits": transits
        })

def journey(start_lat, start_long, end_lat, end_long):
    if abs(start_lat - end_lat) > 0.100 or abs(end_long - start_long) > 0.001:

        max_distance_km = 2

        transit_within_range = []

        # Convert the user's start latitude and longitude from degrees to radians
        current_latitude_rad = radians(start_lat)
        current_longitude_rad = radians(start_long)

        transit_locations = [i.location for i in Transit.objects.all()]

        for location in transit_locations:

            # Convert the location's latitude and longitude from degrees to radians
            location_latitude_rad = radians(location.latitude)
            location_longitude_rad = radians(location.longitude)

            # Calculate the differences between coordinates
            d_latitude = location_latitude_rad - current_latitude_rad
            d_longitude = location_longitude_rad - current_longitude_rad

            # Use Haversine formula to calculate the distance between the two points
            a = sin(d_latitude / 2) ** 2 + cos(current_latitude_rad) * cos(location_latitude_rad) * sin(d_longitude / 2) ** 2
            c = 2 * atan2(sqrt(a), sqrt(1 - a))
            distance_km = 6371.01 * c  # Radius of the Earth in kilometers

            # Check if the location is within the specified distance
            if distance_km <= max_distance_km:
                transit_within_range.append(Transit.objects.get(location=location))

        return transit_within_range




def driver_dashboard(request):
    try:
        Driver.objects.get(user=request.user)
    except Driver.DoesNotExist:
        return HttpResponseRedirect("index")
    
    return render(request, "transit/driver_dashboard.html")

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

def driver_register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        latitude = request.POST["lat"]
        longitude = request.POST["long"]
        seats = request.POST["seats"]
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
            driver = Driver(user=user, available_seats=seats)
            driver.save()
        except IntegrityError:
            return render(request, "transit/driver_register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "transit/driver_register.html")



def custom_404(request):
    return render(request, "transit/404.html", status=404)