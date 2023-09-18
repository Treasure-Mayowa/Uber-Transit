from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    pass
    
class Driver(models.Model):
    pass

class Location(models.Model):
    pass

class Transit(models.Model):
    pass