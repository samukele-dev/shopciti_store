# shopciti_app/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Store
from .models import StoreProfile

@receiver(post_save, sender=Store)
def create_store_profile(sender, instance, created, **kwargs):
    if created:
        StoreProfile.objects.create(store=instance)

@receiver(post_save, sender=Store)
def save_store_profile(sender, instance, **kwargs):
    instance.storeprofile.save()
