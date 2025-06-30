from django.db import models

class Catagory(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField

class Event(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=200)
    category = models.ForeignKey(Catagory, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
class Participant(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    events = models.ManyToManyField(Event, related_name='participants')

    def __str__(self):
        return self.name