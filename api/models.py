from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class User(AbstractUser):
    ROLE_CHOICES = [('N', 'Nurse'), ('D', 'Doctor')]
    GENDER_CHOICES = [('M', 'Male'), ('F', 'Female')]
    username = models.CharField('Username', max_length=255, unique=True)
    email = models.EmailField('Email', unique=True)
    role = models.CharField(max_length=255, choices=ROLE_CHOICES, default='N')
    gender = models.CharField(max_length=255, choices=GENDER_CHOICES, default='M')

    def __str__(self):
        return self.username
