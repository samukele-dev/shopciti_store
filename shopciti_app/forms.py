from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from .models import CustomUser, Product, AdditionalImage, SupportTicket, PaymentMethod, BillingAddress, Size, Category
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




class VendorRegistrationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', 'phone_number', 'country', 'address', 'city', 'postal_code', 'logo', 'password1', 'password2')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

class BuyerRegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'phone_number' , 'email', 'password1', 'password2')




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



class SupportTicketForm(forms.ModelForm):
    class Meta:
        model = SupportTicket
        fields = ['first_name', 'email', 'phone_number', 'description']

class PaymentMethodForm(forms.ModelForm):
    class Meta:
        model = PaymentMethod
        fields = ['card_number', 'card_holder_name', 'expiry_date', 'cvv']
        widgets = {
            'expiry_date': forms.DateInput(attrs={'type': 'date'}),
            'cvv': forms.PasswordInput(),
        }

    def clean_card_number(self):
        card_number = self.cleaned_data['card_number']
        # Implement any validation logic for card number if needed
        return card_number


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
