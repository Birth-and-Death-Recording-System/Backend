# Generated by Django 5.0.2 on 2024-03-04 14:50

import django.db.models.deletion
import django_countries.fields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_alter_profile_birth_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='Birth',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('CIN', models.CharField(max_length=50, unique=True, verbose_name='CIN')),
                ('First_Name', models.CharField(max_length=255, verbose_name='Name')),
                ('Last_Name', models.CharField(max_length=255, verbose_name='Name')),
                ('Other_Name', models.CharField(max_length=255, verbose_name='Name')),
                ('date_of_birth', models.DateField(verbose_name='Date of Birth')),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female')], default='M', max_length=255)),
                ('City', models.CharField(max_length=255, unique=True, verbose_name='City')),
                ('Place_of_Birth', models.CharField(max_length=255, unique=True, verbose_name='State')),
                ('Informant_name', models.CharField(max_length=255, verbose_name='Informant Name')),
                ('Relationship', models.CharField(choices=[('P', 'Parent'), ('S', 'Sibling'), ('Se', 'Self'), ('G', 'Guardian'), ('O', 'Other')], max_length=255, verbose_name='Relationship')),
                ('Father_First_Name', models.CharField(max_length=255, verbose_name='Father Name')),
                ('Father_Last_Name', models.CharField(max_length=255, verbose_name='Father Name')),
                ('Father_Nationality', django_countries.fields.CountryField(max_length=255, verbose_name='Nationality')),
                ('Father_ID_type', models.CharField(choices=[('G', 'Ghana Card'), ('V', "Voter's ID"), ('N', 'NHIS'), ('D', "Driver's License"), ('P', 'Passport')], max_length=255, verbose_name='ID Type')),
                ('Father_ID_Number', models.CharField(max_length=255, unique=True, verbose_name='ID Number')),
                ('Father_DOB', models.DateField(max_length=255, verbose_name='Age')),
                ('Mother_First_Name', models.CharField(max_length=255, verbose_name='Mother Name')),
                ('Mother_Last_Name', models.CharField(max_length=255, verbose_name='Mother Name')),
                ('Mother_Nationality', django_countries.fields.CountryField(max_length=255, verbose_name='Nationality')),
                ('Mother_ID_type', models.CharField(choices=[('G', 'Ghana Card'), ('V', "Voter's ID"), ('N', 'NHIS'), ('D', "Driver's License"), ('P', 'Passport')], max_length=255, verbose_name='ID Type')),
                ('Mother_ID_number', models.CharField(max_length=255, unique=True, verbose_name='ID Number')),
                ('Mother_DOB', models.DateField(max_length=255, verbose_name='Age')),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='birth', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
