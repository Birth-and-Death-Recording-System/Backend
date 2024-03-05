from django.contrib import admin
from .models import User, Profile, Birth, Death

# Register your models here.
admin.site.register(User)
admin.site.register(Profile)
admin.site.register(Birth)
admin.site.register(Death)
