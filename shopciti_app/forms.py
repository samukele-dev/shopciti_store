from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Product
from django import forms



class SellerApplicationForm(forms.Form):
    email = forms.EmailField()
    phone = forms.CharField(max_length=15)
    shop_name = forms.CharField(max_length=100)  # Add the shop_name field
    address = forms.CharField(widget=forms.Textarea)
    agreed_to_terms = forms.BooleanField()

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")


# /////////////////////////////////////////////////////////////////////////////////




class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(max_length=254, required=True)
    phone = forms.CharField(max_length=15, required=True)
    country = forms.CharField(max_length=100, required=True)
    address = forms.CharField(max_length=255, required=True)
    city = forms.CharField(max_length=100, required=True)
    postcode = forms.CharField(max_length=10, required=True)
    
    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', 'phone', 'country', 'address', 'city', 'postcode', 'password1', 'password2')


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'image', 'price']

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


class PayFastForm(forms.Form):
    # Define the form fields for PayFast
    merchant_id = forms.CharField(initial='23353254')
    merchant_key = forms.CharField(initial='r7cx2yvt9i7gf')
    return_url = forms.URLField()
    cancel_url = forms.URLField()
    notify_url = forms.URLField()
    email_address = forms.EmailField()
    cell_number = forms.CharField()
    m_payment_id = forms.CharField()
    amount = forms.DecimalField()
    item_name = forms.CharField()
