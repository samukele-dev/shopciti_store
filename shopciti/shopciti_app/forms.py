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


