from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings


class CustomUser(AbstractUser):
    about = models.TextField(blank=True, null=True)
    profile_image = models.ImageField(upload_to='profile_image/', blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100, default='South Africa')
    postal_code = models.CharField(max_length=20, default='000000000')
    class Meta:
        app_label = 'shopciti_app'


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='product_images/')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    added_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=None, blank=True, null=True)

    def __str__(self):
        return self.name


User = get_user_model()

class VendorApplication(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='vendor_applications')
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    shop_name = models.CharField(max_length=100)
    address = models.TextField()
    agreed_to_terms = models.BooleanField(default=False)

    def __str__(self):
        return f"Vendor Application for {self.user.username}"
