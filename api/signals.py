from django.db.models.signals import post_save, post_delete
from .models import User, Profile, DeathRecord
from django.dispatch import receiver
from .models import BirthRecord, Birth, Death


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


@receiver(post_save, sender=Birth)
def log_birth_record_creation(sender, instance, created, **kwargs):
    action_type = 'Birth recorded' if created else 'Birth updated'

    # details = f"{action_type}: Birth of '{instance.First_Name} {instance.Last_Name}' recorded by '{instance.user.username}' at {instance.date} in {instance.Place_of_Birth}."
    details1 = f"{action_type}: {instance.user.username} - {instance.First_Name}"
    BirthRecord.objects.create(
        recorder=instance.user,
        birth=instance,
        action_type=action_type,
        details=details1
    )


@receiver(post_save, sender=Death)
def log_death_record_creation(sender, instance, created, **kwargs):
    action_type = 'Death recorded' if created else 'Death updated'

    # details = f"{action_type}: Death of '{instance.first_name} {instance.surname}' recorded by '{instance.user.username}' at {instance.date} in {instance.Place_of_Death}."
    details1 = f"{action_type}: {instance.user.username} - {instance.first_name}"
    DeathRecord.objects.create(
        recorder=instance.user,
        death=instance,
        action_type=action_type,
        details=details1
    )


@receiver(post_delete, sender=Birth)
def log_birth_record_deletion(sender, instance, **kwargs):
    BirthRecord.objects.create(
        recorder=instance.user,
        action_type='Birth deleted',
        details=f"Birth record for '{instance.First_Name} {instance.Last_Name}' was deleted."
    )


@receiver(post_delete, sender=Death)
def log_death_record_deletion(sender, instance, **kwargs):
    if instance:
        DeathRecord.objects.create(
            recorder=instance.user,
            action_type='Death deleted',
            details=f"Death deleted: {instance.user.username} - {instance.first_name}"
        )
