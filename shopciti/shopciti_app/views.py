from .models import Product
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Store  # Import the Store model if you have it
from django.contrib.auth.decorators import login_required
from .models import Store, StoreProfile
from .forms import CustomUserCreationForm
from django.core.exceptions import ObjectDoesNotExist
from .forms import UserProfileForm, StoreForm, CartAddProductForm, ProductForm
from django.core.paginator import Paginator
from django.db.models import Q




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

def home2(request):
    return render(request, 'shopciti_app/home2.html')

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
        form = StoreForm(request.POST, request.FILES)  # Include request.FILES to handle file uploads
        if form.is_valid():
            new_store = form.save()
            user = request.user
            user.store = new_store
            user.save()
            return redirect('store_profile')
    else:
        form = StoreForm()

    return render(request, 'shopciti_app/register_store.html', {'form': form})


def registration_success(request):
    # Render the registration success or thank you page
    return render(request, 'registration_success.html')

def registration_failure(request):
    # Render a page indicating registration failure with appropriate message
    return render(request, 'shopciti_app/registration_failure.html')



def shop_list(request):
    search_query = request.GET.get('search_query', '')
    category = request.GET.get('category', '')
    sort_by = request.GET.get('sort_by', 'name')
    

    # Use Q objects to create complex queries for searching
    filter_criteria = Q(name__icontains=search_query)

    # Add more fields as needed to search in other attributes of the Store model
    if category:
        filter_criteria |= Q(category__icontains=category)

    if not sort_by:
        sort_by = 'name'  # Set a default sorting option if 'sort_by' is empty
    shops = Store.objects.filter(filter_criteria).order_by(sort_by)

    paginator = Paginator(shops, 10)
    page = request.GET.get('page')
    shops = paginator.get_page(page)

    context = {
        'shops': shops,
    }
    return render(request, 'shopciti_app/shop_list.html', context)


@login_required
def shop_detail(request, shop_id):
    shop = get_object_or_404(Store, pk=shop_id)
    products = Product.objects.filter(store=shop)
    return render(request, 'shopciti_app/shop_detail.html', {'shop': shop, 'products': products})
    


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


def product_list(request):
    products = Product.objects.all()
    return render(request, 'shopciti_app/product_list.html', {'products': products})

def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cart.add(product=product, quantity=form.cleaned_data['quantity'])
    return redirect('cart')

def cart(request):
    cart = Cart(request)
    return render(request, 'shopciti_app/cart.html', {'cart': cart})

def remove_from_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    cart.remove(product)
    return redirect('cart')

def update_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cart.update(product=product, quantity=form.cleaned_data['quantity'])
    return redirect('cart')

def checkout(request):
    cart = Cart(request)
    # Implement the checkout process here
    return render(request, 'shopciti_app/checkout.html', {'cart': cart})

def order_confirmation(request):
    # Handle order confirmation logic here
    return render(request, 'shopciti_app/order_confirmation.html')


@login_required
def manage_products(request, store_id):
    # Get the store object by its ID or return a 404 if not found
    store = get_object_or_404(Store, pk=store_id)

    # Retrieve all products associated with the store
    products = Product.objects.filter(store=store)

    return render(request, 'shopciti_app/product_template/manage_products.html', {'store': store, 'products': products})


@login_required
# Add a new product to the store

def add_product_to_store(request, store_id):
    store = get_object_or_404(Store, pk=store_id)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            new_product = form.save(commit=False)
            new_product.store = store
            new_product.save()
            return redirect(reverse('manage_products', kwargs={'store_id': store_id}))
    else:
        form = ProductForm()

    return render(request, 'shopciti_app/product_template/add_product.html', {'form': form, 'store_id': store_id})

# Edit an existing product
def edit_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect(reverse('manage_products', kwargs={'store_id': product.store.id}))
    else:
        form = ProductForm(instance=product)

    return render(request, 'shopciti_app/product_template/edit_product.html', {'form': form, 'store_id': product.store.id})
# Delete an existing product
def delete_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    store_id = product.store.id
    product.delete()
    return redirect('manage_products', store_id=store_id)


