# signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Teacher, Profile

@receiver(post_save, sender=Teacher)
def create_or_update_profile(sender, instance, created, **kwargs):
    if created:
        # Create a Profile associated with the Teacher's user
        Profile.objects.create(user=instance.user)
    else:
        # Update the existing profile if needed
        instance.user.profile.save()
