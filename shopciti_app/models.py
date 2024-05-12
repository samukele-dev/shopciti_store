

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings


class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=30, default='')
    last_name = models.CharField(max_length=30, default='')
    about = models.TextField(blank=True, null=True)
    logo = models.ImageField(upload_to='profile_image/', blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField()
    country = models.CharField(max_length=50, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100, default='South Africa')
    postal_code = models.CharField(max_length=20, default='0000')
    phone = models.CharField(max_length=15, default='')  # Provide a default empty string
    
    is_buyer = models.BooleanField(default=False)


    class Meta:
        app_label = 'shopciti_app'


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
Category.objects.create(name='Hoodie')
Category.objects.create(name='Sweater')
Category.objects.create(name='Pants')
Category.objects.create(name='T.shirt')
Category.objects.create(name='Shirt')
Category.objects.create(name='Hat, cap')


class Product(models.Model):
    name = models.CharField(max_length=100)
    short_description = models.TextField(default='')  # Provide a default empty string
    description = models.TextField()
    image = models.ImageField(upload_to='product_images/')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    added_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=None, blank=True, null=True)
    on_sale = models.BooleanField(default=False)
    categories = models.ManyToManyField(Category)

    available = models.PositiveIntegerField(default=True)  # assuming it can't be negative


    def __str__(self):
        return self.name



class RelatedProduct(models.Model):
    main_product = models.ForeignKey(Product, related_name='related_products', on_delete=models.CASCADE)
    related_product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.main_product.name} - {self.related_product.name}"


class ProductVariant(models.Model):
    product = models.ForeignKey(Product, related_name='variants', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='product_variant_images/', blank=True, null=True)
    size = models.CharField(max_length=50, blank=True, null=True)
    color = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{self.product.name} - {self.name}"


class AdditionalImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='additional_images')
    image = models.ImageField(upload_to='additional_images/')
    added_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=None, blank=True, null=True)

    def __str__(self):
        return f"Additional Image for {self.product.name} by {self.added_by.username}"


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


class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def get_total_price(self):
        return self.product.price * self.quantity

class BillingAddress(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    country = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.first_name} {self.last_name}'s Billing Address"