# Generated by Django 5.0.2 on 2024-09-22 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0026_alter_profile_gender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='phone_number',
            field=models.CharField(blank=True, default=0, max_length=10, unique=True, verbose_name='Phone Number'),
        ),
    ]
