from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth import get_user_model


class Store(models.Model):
    SUBSCRIPTION_CHOICES = [
        ("free", "Free"),
        ("basic", "Basic"),
        ("premium", "Premium"),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    contact_email = models.EmailField(blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    postal_code = models.CharField(max_length=10, blank=True, null=True)
    logo = models.ImageField(upload_to='store_logos/', default='static/img/1.png')
    about = models.TextField(blank=True, null=True)
    
    subscription_level = models.CharField(max_length=10, choices=SUBSCRIPTION_CHOICES, default="free")

    def __str__(self):
        return self.name

class CustomUser(AbstractUser):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, null=True, blank=True)
    about = models.TextField(blank=True, null=True)
    profile_image = models.ImageField(upload_to='profile_image/', blank=True, null=True)

    class Meta:
        app_label = 'shopciti_app'


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

    # Add a foreign key to the Store model to represent the relationship
    store = models.ForeignKey(Store, on_delete=models.CASCADE, null=True)  # Add this ForeignKey

    def __str__(self):
        return self.name

class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)





class Review(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    rating = models.IntegerField()  # You can use a rating field or create a separate model for ratings
    comment = models.TextField()
