# Generated by Django 5.0.2 on 2024-04-06 09:16

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0023_alter_birth_father_nationality_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='birth',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL),
        ),
    ]
