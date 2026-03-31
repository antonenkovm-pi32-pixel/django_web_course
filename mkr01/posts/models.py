from django.db import models
from django.contrib import admin
from django.utils.html import format_html

# Create your models here.

class Post(models.Model):
    text=models.TextField()
    data=models.DateTimeField()
    temperature=models.FloatField()
    pressure=models.FloatField()
    speed = models.FloatField()
    probability = models.FloatField()
    
class PostAdmin(admin.ModelAdmin):
    list_display=["text", "data", "temperature", "pressure", "speed", "probability"]