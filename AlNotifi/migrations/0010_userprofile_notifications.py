# Generated by Django 5.0 on 2024-01-19 19:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AlNotifi', '0009_notifications'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='notifications',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to='AlNotifi.notifications'),
        ),
    ]
