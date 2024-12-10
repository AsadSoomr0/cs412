"""
signals.py
Author: Asad Soomro
Email: asoomro@bu.edu

This file contains signal handlers for the Rock City web application. It includes
a post-save signal for the User model to automatically create or update a Profile
instance whenever a User instance is created or saved.
"""
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        # Create a Profile instance if the User is being created
        Profile.objects.create(user=instance)
    else:
        # Save the Profile instance if it already exists
        if hasattr(instance, 'profile'):
            instance.profile.save()