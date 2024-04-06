# Generated by Django 5.0.2 on 2024-04-06 22:58

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0024_alter_birth_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='death',
            name='Nationality',
            field=models.CharField(max_length=255, verbose_name='Nationality'),
        ),
        migrations.AlterField(
            model_name='death',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='deaths', to=settings.AUTH_USER_MODEL),
        ),
    ]