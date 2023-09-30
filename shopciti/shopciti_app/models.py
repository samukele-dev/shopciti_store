from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import User  # If using Django's built-in User model


class Store(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    contact_email = models.EmailField(blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    postal_code = models.CharField(max_length=10, blank=True, null=True)
    
    # Add profile-related fields here
    profile_image = models.ImageField(upload_to='store_profiles/', blank=True, null=True)
    about = models.TextField(blank=True, null=True)

    # Add more fields as needed to store store-related information.

    def __str__(self):
        return self.name

class CustomUser(AbstractUser):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, null=True, blank=True)

    # Add a related_name to avoid clashes
    groups = models.ManyToManyField(
        "auth.Group",
        blank=True,
        related_name="customuser_set",
        related_query_name="customuser",
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        blank=True,
        related_name="customuser_set",
        related_query_name="customuser",
    )
    
class StoreProfile(models.Model):
    store = models.OneToOneField(Store, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    logo = models.ImageField(upload_to='store_logos/', blank=True, null=True)

    def __str__(self):
        return self.store.name

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/')

    def __str__(self):
        return self.name

