from django.db import models
from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse

# Create your models here.

class Post(models.Model):
    text=models.TextField()
    data=models.DateTimeField()
    temperature=models.FloatField()
    pressure=models.FloatField()
    speed = models.FloatField()
    probability = models.FloatField()
    title = models.CharField(max_length=200)
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)

    def __str__(self):
        return self.text
    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk': self.pk})

    
class PostAdmin(admin.ModelAdmin):
    list_display=["text", "data", "temperature", "pressure", "speed", "probability"]