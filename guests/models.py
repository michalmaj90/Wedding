from django.db import models

FOOD = (
    (1, 'Normalne'),
    (2, 'Wegetariańskie')
)
# Create your models here.

class WeddingCouple(models.Model):
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    description = models.CharField(max_length=300)
    email = models.CharField(max_length=64)
    phone = models.IntegerField()

class WeddingGuest(models.Model):
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    email = models.CharField(max_length=64)
    phone = models.IntegerField()
    food = models.IntegerField(choices=FOOD)

class AccompanyingPerson(models.Model):
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    food = models.IntegerField(choices=FOOD)
    companion = models.OneToOneField(WeddingGuest, on_delete=models.CASCADE, primary_key=True)

class WeddingInfo(models.Model):
    church_name = models.CharField(max_length=200)
    church_address = models.CharField(max_length=200)
    church_view = models.CharField(max_length=300, null=True)
    premises_name = models.CharField(max_length=200)
    premises_address = models.CharField(max_length=200)
    premises_view = models.CharField(max_length=300, null=True)
