from django.db import models
from django.contrib.auth.models import User

FOOD = (
    ("Normalne", 'Normalne'),
    ("Wegetariańskie", 'Wegetariańskie')
)
# Create your models here.

class WeddingCouple(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    first_name = models.CharField(max_length=64, default="", blank=True)
    last_name = models.CharField(max_length=64, default="", blank=True)
    description = models.CharField(max_length=300, default="", blank=True)
    email = models.EmailField(max_length=64, default="", blank=True)
    phone = models.IntegerField(blank=True, null=True)

class WeddingGuest(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    first_name = models.CharField(max_length=64, blank=True)
    last_name = models.CharField(max_length=64, blank=True)
    email = models.EmailField(max_length=64, blank=True)
    phone = models.IntegerField(blank=True, null=True)
    food = models.CharField(max_length=64, choices=FOOD, null=True)

class AccompanyingPerson(models.Model):
    first_name = models.CharField(max_length=64, blank=True)
    last_name = models.CharField(max_length=64, blank=True)
    food = models.CharField(max_length=64, choices=FOOD)
    companion = models.OneToOneField(WeddingGuest, on_delete=models.CASCADE, primary_key=True)

class WeddingInfo(models.Model):
    church_name = models.CharField(max_length=200, blank=True)
    church_address = models.CharField(max_length=200, blank=True)
    church_view = models.TextField(max_length=300, blank=True)
    premises_name = models.CharField(max_length=200, blank=True)
    premises_address = models.CharField(max_length=200, blank=True)
    premises_view = models.TextField(max_length=300, blank=True)
