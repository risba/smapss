from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.

class Profile(models.Model):
    profile_name = models.CharField(max_length=100, null=True, blank=True)
    score = models.FloatField(null=True, blank=True)

class Feedback(models.Model):
    feedback = models.TextField(null=True, blank=True, max_length=1000)

class Prediction(models.Model):
    user = models.CharField(max_length=100, null=True, blank=True)
    prediction_date = models.DateField(null=True, blank=True)
    stock_name = models.CharField(max_length=100, null=True, blank=True)
    buy_price = models.FloatField(null=True, blank=True)
    sell_price = models.FloatField(null=True, blank=True)
    money_amount = models.FloatField(null=True, blank=True)
