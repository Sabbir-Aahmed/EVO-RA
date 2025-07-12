from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Catagory(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField(blank=True,null=True)

    def __str__(self):
        return self.name

class Event(models.Model):
    name = models.CharField(max_length=250) 
    image = models.ImageField(upload_to='events_image', blank=True, null= True, default= "events_image/default.jpg")
    description = models.TextField()
    date = models.DateField(default=timezone.now)
    time = models.TimeField(default=timezone.now)
    location = models.CharField(max_length=200)
    category = models.ForeignKey(Catagory, on_delete=models.CASCADE)
    participants = models.ManyToManyField(User, related_name='events')
    def __str__(self):
        return self.name
    
    def is_upcoming(self):
        return self.date >= timezone.now().date()

    def is_today(self):
        return self.date == timezone.now().date()
    