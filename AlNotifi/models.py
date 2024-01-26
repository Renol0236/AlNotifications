from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class DiscordProfile(models.Model):
    id = models.BigIntegerField(primary_key=True)
    discord_tag = models.CharField(max_length=100)
    avatar = models.CharField(max_length=100, null=True)
    public_flags = models.IntegerField()
    flags = models.IntegerField()
    global_name = models.CharField(max_length=100, null=True)
    locale = models.CharField(max_length=100)
    mfa_enabled = models.BooleanField()
    last_login = models.DateTimeField()

class Notifications(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    message = models.TextField(max_length=500)
    time = models.DateTimeField()
    is_sent = models.BooleanField(default=False)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    discord_profile = models.OneToOneField(DiscordProfile, on_delete=models.CASCADE, blank=True, null=True)
    bio = models.TextField(max_length=250, blank=True)
    phone = models.BigIntegerField(blank=True, null=True)
    full_name = models.CharField(blank=True, null=True)
    address = models.CharField(blank=True, null=True)

    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def __str__(self):
        return self.user.username


