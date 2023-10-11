from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django import forms
from .models import StoreProfile, Store, Product


class StoreForm(forms.ModelForm):
    logo = forms.ImageField(label='Store Logo', required=False)  # Add this line

    class Meta:
        model = Store
        fields = ['name', 'state', 'address', 'city', 'postal_code', 'phone_number', 'contact_email','logo']


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'image']

class StoreProfileForm(forms.ModelForm):
    class Meta:
        model = StoreProfile  # Use the StoreProfile model
        fields = ['description', 'logo']
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'profile_image', 'about']

class CartAddProductForm(forms.Form):
    quantity = forms.IntegerField(
        widget=forms.TextInput(attrs={'type': 'number', 'min': '1', 'value': '1'}),
        min_value=1
    )


class CheckoutForm(forms.Form):
    full_name = forms.CharField(max_length=100, required=True)
    address = forms.CharField(max_length=200, required=True)
    city = forms.CharField(max_length=100, required=True)
    # Add more fields as needed for the checkout process, such as email, phone, etc.
    
    # Payment Information
    card_number = forms.CharField(label='Credit Card Number', max_length=16, required=True)
    cardholder_name = forms.CharField(label='Cardholder Name', max_length=100, required=True)
    expiration_date = forms.CharField(label='Expiration Date (MM/YY)', max_length=5, required=True)
    cvv = forms.CharField(label='CVV', max_length=4, required=True)