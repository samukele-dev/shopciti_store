from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django import forms
from .models import Store

class StoreProfileForm(forms.ModelForm):
    class Meta:
        model = Store
        fields = ['description', 'contact_email', 'phone_number', 'address', 'city', 'state', 'postal_code']

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')