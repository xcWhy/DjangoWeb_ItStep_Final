from django.db import models
from django.contrib.auth.models import User

# Create your models here.
#w are going to be working with cclases as tables in the db
#when we make a new model fo the db we need to migrate - to build a migration
# makemigrations -> migrate


class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    

class Ingredient(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    
    name = models.CharField(max_length=200)
    
    bio = models.TextField(null=True, blank=True)  
    description = models.TextField(null=True, blank=True)  # cooking method
    ingredients = models.TextField(null=True, blank=True)  # list of ingredients
    
    image = models.ImageField(upload_to='recipe_images/', null=True, blank=True)

    update = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-update', '-created']

    def __str__(self):
        return self.name

# 1 to many db
class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE) # fi the room is deleted all of the children i nthat room will be deleted too
    body = models.TextField()
    update = models.DateTimeField(auto_now=True) # takse a snapshot everytime we save
    created = models.DateTimeField(auto_now_add=True) # takse a snapshot only when we created this

    def __str__(self):
        return self.body[0:50] #w return the first 50 elements