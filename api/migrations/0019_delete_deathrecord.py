# Generated by Django 5.0.2 on 2024-03-18 14:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0018_rename_user_deathrecord_recorder_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='DeathRecord',
        ),
    ]
