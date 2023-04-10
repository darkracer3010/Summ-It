from django.db import models

# Create your models here.
class users(models.Model):
    email=models.EmailField(primary_key=True)
    username=models.CharField(max_length=20)
    phone=models.IntegerField()
    password=models.CharField(max_length=20)