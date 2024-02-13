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


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    first_name = models.CharField('First Name', max_length=255)
    last_name = models.CharField('Last Name', max_length=255)
    username = models.CharField('Username', max_length=255, unique=True)
    birth_date = models.DateField('Birth', blank=True, null=True)
    email = models.EmailField('Email', null=False)
    phone_number = models.CharField('Phone Number', max_length=10, blank=True)
    gender = models.CharField('Gender', max_length=10)
    profile_pic = models.ImageField('Profile, Image', upload_to='profile_pics', default='default.jpg')

    def __str__(self):
        return f'{self.user.username} Profile'
