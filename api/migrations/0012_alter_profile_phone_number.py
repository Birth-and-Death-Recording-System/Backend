# Generated by Django 5.0.2 on 2024-03-05 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_birth_father_phone_number_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='phone_number',
            field=models.IntegerField(blank=True, default=0, verbose_name='Phone Number'),
        ),
    ]