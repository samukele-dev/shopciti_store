from .models import Product

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Store  # Import the Store model if you have it
from django.contrib.auth.decorators import login_required
from .models import Store, StoreProfile
from .forms import CustomUserCreationForm
from django.core.exceptions import ObjectDoesNotExist
from .forms import UserProfileForm






def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('user_profile')  # Redirect to the user's profile page
    else:
        form = CustomUserCreationForm()
    return render(request, 'shopciti_app/register.html', {'form': form})


def product_list(request):
    products = Product.objects.all()
    return render(request, 'shopciti_app/product_list.html', {'products': products})

def home(request):
    return render(request, 'shopciti_app/home.html')

@login_required
def user_profile(request):
    user = request.user  # This is your custom user model
    try:
        store = user.store  # Access the store associated with the custom user
    except ObjectDoesNotExist:
        # Handle the case where the custom user or store does not exist
        return redirect('registration_failure')

    try:
        store_profile = StoreProfile.objects.get(store=store)
    except ObjectDoesNotExist:
        # Handle the case where the store profile does not exist
        store_profile = None

    # Check if the user has uploaded a profile image
    profile_image_url = None
    if user.profile_image and user.profile_image.url:
        profile_image_url = user.profile_image.url

    return render(request, 'shopciti_app/user_profile.html', {'user': user, 'store': store, 'store_profile': store_profile, 'profile_image_url': profile_image_url})

@login_required
def edit_profile(request):
    user = request.user

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user)

        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully.')
            return redirect('user_profile')
    else:
        form = UserProfileForm(instance=user)

    return render(request, 'shopciti_app/edit_profile.html', {'form': form})

@login_required
def register_store(request):
    if request.method == 'POST':
        store_name = request.POST['store_name']
        # Process the form data and store it in the database
        # Replace this section with your actual database logic
        try:
            # Create a new Store object and save it to the database
            new_store = Store(name=store_name)
            new_store.save()

            # Link the newly created store to the user
            user = request.user
            user.store = new_store
            user.save()

            # Redirect to a thank you or confirmation page
            return redirect('store_profile')

        except Exception as e:
            # Handle exceptions, such as database errors, here
            messages.error(request, f'An error occurred while registering your store: {str(e)}')
            return redirect('registration_failure')

    # Render the store registration form page if it's a GET request
    return render(request, 'shopciti_app/register_store.html')

def registration_success(request):
    # Render the registration success or thank you page
    return render(request, 'registration_success.html')

def registration_failure(request):
    # Render a page indicating registration failure with appropriate message
    return render(request, 'shopciti_app/registration_failure.html')



def shop_list(request):
    stores = Store.objects.all()
    return render(request, 'shops.html', {'stores': stores})



@login_required
def store_profile(request):
    user = request.user  # This is your custom user model
    try:
        store = user.store  # Access the store associated with the custom user
    except ObjectDoesNotExist:
        # Handle the case where the custom user or store does not exist
        return redirect('registration_failure')

    try:
        store_profile = StoreProfile.objects.get(store=store)
    except ObjectDoesNotExist:
        # Handle the case where the store profile does not exist
        store_profile = None

    return render(request, 'shopciti_app/store_profile.html', {'store': store, 'store_profile': store_profile})