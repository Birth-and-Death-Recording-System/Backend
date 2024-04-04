# Generated by Django 5.0.2 on 2024-03-18 14:56

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0019_delete_deathrecord'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeathRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recorded_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('action_type', models.CharField(default='Death recorded', max_length=50)),
                ('details', models.TextField(blank=True, null=True)),
                ('death', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.death')),
                ('recorder', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]