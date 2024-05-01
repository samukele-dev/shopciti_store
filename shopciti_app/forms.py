from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from .models import CustomUser, Product, AdditionalImage, BillingAddress
from django import forms
from django.forms import inlineformset_factory



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
    logo = forms.ImageField(required=True)

    old_password = forms.CharField(widget=forms.HiddenInput(), required=False)  # Make the old password field hidden
    new_password1 = forms.CharField(widget=forms.HiddenInput(), required=False)  # Make the new password field hidden
    new_password2 = forms.CharField(widget=forms.HiddenInput(), required=False)  # Make the confirm new password field hidden

    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', 'phone', 'country', 'address', 'city', 'postcode', 'logo')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class BuyerRegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'password1', 'password2', 'email', 'first_name', 'last_name', 'phone')


class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].required = True  # Ensure old_password field is required



class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'image', 'price', 'on_sale']

        widgets = {
            'on_sale': forms.Select(choices=[(True, 'Yes'), (False, 'No')]),
        }


class AdditionalImageForm(forms.ModelForm):
    class Meta:
        model = AdditionalImage
        fields = ['image']

AdditionalImageFormSet = inlineformset_factory(Product, AdditionalImage, form=AdditionalImageForm, extra=3, max_num=5, can_delete=True)

class CartAddProductForm(forms.Form):
    quantity = forms.IntegerField(
        widget=forms.TextInput(attrs={'type': 'number', 'min': '1', 'value': '1'}),
        min_value=1
    )


class BillingAddressForm(forms.ModelForm):
    class Meta:
        model = BillingAddress
        fields = ['first_name', 'last_name', 'email', 'phone', 'country', 'address', 'city', 'postal_code']

class CheckoutForm(forms.Form):
    full_name = forms.CharField(max_length=100, required=True)
    address = forms.CharField(max_length=200, required=True)
    city = forms.CharField(max_length=100, required=True)
    
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
