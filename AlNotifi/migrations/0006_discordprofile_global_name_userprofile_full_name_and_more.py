# Generated by Django 5.0 on 2024-01-18 19:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AlNotifi', '0005_alter_userprofile_bio'),
    ]

    operations = [
        migrations.AddField(
            model_name='discordprofile',
            name='global_name',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='full_name',
            field=models.CharField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='phone',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
