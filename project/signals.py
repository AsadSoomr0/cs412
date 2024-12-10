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