from django.conf import settings
from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Room(models.Model):
    name = models.CharField(max_length = 255, unique=True)
    
    def __str__(self):
        return self.name
    
class Message(models.Model):
    room =  models.ForeignKey(Room, on_delete= models.CASCADE)
    user =  models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']