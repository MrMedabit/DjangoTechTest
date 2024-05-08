from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class EventIntegerChoices(models.IntegerChoices):
    PRODUCT = 1
    USER= 2

class CustomUser(AbstractUser):
    level = models.IntegerField(default=2, blank=False)

class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    description = models.CharField(blank=True)
    quantity = models.IntegerField(default=1)
    date_added = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=1)

class Event(models.Model):
    id = models.AutoField(primary_key=True)
    event_type = models.IntegerField(choices=EventIntegerChoices ,blank=False)
    description = models.CharField(max_length=200, blank=False)
    creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=None)
    date = models.DateTimeField(auto_now=True)