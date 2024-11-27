# tracker/models.py
from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=[
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ])
    bio = models.TextField(blank=True)

class MoodEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    mood = models.CharField(max_length=20, choices=[
        ('Happy', 'Happy'),
        ('Sad', 'Sad'),
        ('Anxious', 'Anxious'),
        ('Neutral', 'Neutral'),
        ('Angry', 'Angry'),
    ])
    note = models.TextField(blank=True)

class Activity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    date = models.DateField()
    description = models.TextField(blank=True)
