from django.db import models

# Create your models here.

class Dog(models.Model):
    breed = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    is_friendly = models.BooleanField(default=True)
    
    