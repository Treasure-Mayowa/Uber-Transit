from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Location(models.Model):
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)

    def __str__(self):
        return f"{self.latitude}° lat and {self.longitude}° long" 


class User(AbstractUser):
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="location")
    driver = models.BooleanField(default=False)
    

class Transit(models.Model):
    name = models.CharField(max_length=150)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="routes")
    transit_type = models.CharField(max_length=50)