from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

# Create your models here.
class Location(models.Model):
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.latitude}° lat and {self.longitude}° long" 


class User(AbstractUser):
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="location", default=None, null=True)
    
class Driver(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    available_seats = models.IntegerField(default=0)
    accessibility = models.TextField(default="Nil")

    def __str__(self):
        return f"{self.user.username} at {self.user.location}"
    
class Trips(models.Model):
    passengers = models.ManyToManyField(User)
    time = models.DateTimeField(auto_now_add=True)
    duration = models.DurationField()
    start = models.ForeignKey(Location, on_delete=models.CASCADE)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)

class Ride(models.Model):
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, related_name="rides")
    destination = models.ForeignKey(Location, on_delete=models.CASCADE)
    departure_time = models.DateTimeField(auto_now=True)
    available_seats = models.IntegerField(default=0)
    passengers = models.ManyToManyField(User, related_name="rides_taken", blank=True)

class Transit(models.Model):
    name = models.CharField(max_length=150)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="routes")
    transit_type = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name} in {self.location} ({self.transit_type})"