from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.



class User(AbstractUser):
    name = models.CharField(max_length=30)
    email = models.CharField(max_length=30,unique=True)
    password = models.CharField(max_length=30)

    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class Post(models.Model):
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=100,null=False)
    discription = models.CharField(max_length=250,null=False)
    created_on = models.DateTimeField(auto_now_add=True)

