# Generated by Django 5.0 on 2024-01-17 23:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AlNotifi', '0002_userprofile_delete_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='profile_picture',
            field=models.ImageField(blank=True, null=True, upload_to='profile_pics/'),
        ),
    ]
