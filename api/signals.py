from django.db.models.signals import post_save, post_delete
from .models import User, Profile
from django.dispatch import receiver


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        user = instance
        Profile.objects.create(user=user,
                               username=user.username,
                               email=user.email,
                               first_name=user.first_name,
                               last_name=user.last_name,
                               gender=user.gender)


@receiver(post_save, sender=Profile)
def update_profile(sender, instance, created, **kwargs):
    profile = instance
    user = profile.user
    if not created:
        user.first_name = profile.first_name
        user.last_name = profile.last_name
        user.email = profile.email
        user.gender = profile.gender
        user.save()


@receiver(post_delete, sender=Profile)
def delete_profile(sender, instance, **kwargs):
    user = instance.user
    user.delete()
