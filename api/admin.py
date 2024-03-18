from django.contrib import admin
from .models import User, Profile, Birth, Death, ActionLog, BirthRecord, DeathRecord

# Register your models here.
admin.site.register(User)
admin.site.register(Profile)
admin.site.register(Birth)
admin.site.register(Death)
admin.site.register(ActionLog)
admin.site.register(BirthRecord)
admin.site.register(DeathRecord)
