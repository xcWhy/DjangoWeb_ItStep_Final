from django.contrib import admin

# Register your models here.

from .models import Room, Topic, Message, Ingredient

admin.site.register(Room)
admin.site.register(Topic)
admin.site.register(Message)
admin.site.register(Ingredient)
