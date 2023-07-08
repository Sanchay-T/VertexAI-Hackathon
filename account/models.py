from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import CustomUserManager

# Create your models here.

class CustomUser(AbstractUser):
    username = models.CharField(max_length=250, null=False)

    email = models.EmailField(max_length=250, unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = CustomUserManager()
    user_type_data = ((1 , "HR") , (2 , "Employee"))
    user_type = models.CharField(default=1 , choices=user_type_data , max_length=10)


    def __str__(self):
        return "{}".format(self.username)

