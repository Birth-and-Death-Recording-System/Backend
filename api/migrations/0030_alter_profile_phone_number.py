# Generated by Django 5.0.2 on 2024-09-22 12:26

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0029_alter_profile_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='phone_number',
            field=models.CharField(blank=True, default='', max_length=10, validators=[django.core.validators.MinLengthValidator(10), django.core.validators.RegexValidator(message='Phone number must be 10 digits long and contain only numbers.', regex='^\\d{10}$')], verbose_name='Phone Number'),
        ),
    ]
