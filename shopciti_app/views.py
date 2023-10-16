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
from .forms import UserProfileForm, StoreForm, CartAddProductForm, ProductForm, CheckoutForm
from django.core.paginator import Paginator
from django.db.models import Q
from .cart import Cart
from payfast.forms import PayFastForm
from django.http import HttpResponse



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

def home2(request):
    return render(request, 'shopciti_app/home2.html')

def home1(request):
    return render(request, 'shopciti_app/home1.html')

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


def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return render(request, 'shopciti_app/product_detail.html', {'product': product})

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


# Add a product to the cart
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = request.session.get('cart', {})
    cart_item = cart.get(str(product_id))

    if cart_item:
        cart_item['quantity'] += 1
    else:
        cart_item = {
            'product_id': product_id,
            'name': product.name,
            'price': float(product.price),
            'quantity': 1,
        }

    cart[str(product_id)] = cart_item
    request.session['cart'] = cart
    return redirect('cart')

def cart(request):
    cart = request.session.get('cart', {})
    cart_items = cart.values()
    total_price = sum(float(item['price']) * item['quantity'] for item in cart_items)
    return render(request, 'shopciti_app/cart.html', {'cart_items': cart_items, 'total_price': total_price})


# Remove a product from the cart
def remove_from_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = Cart(request)
    cart.remove(product)
    return redirect('cart')

# Update the quantity of a product in the cart
def update_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == 'POST':
        quantity = request.POST.get('quantity')  # Get the quantity from the form

        # Ensure quantity is a valid integer
        try:
            quantity = int(quantity)
        except ValueError:
            quantity = 1  # Default to 1 if quantity is not a valid integer

        # Retrieve the cart from the session or create an empty one
        cart = request.session.get('cart', {})

        # Update the quantity for the product in the cart
        if product_id in cart and quantity > 0:
            cart[product_id]['quantity'] = quantity
        elif product_id in cart and quantity <= 0:
            del cart[product_id]

        # Save the updated cart back to the session
        request.session['cart'] = cart

    return redirect('cart')


# Checkout view

# Order confirmation view (after successful checkout)
def order_confirmation(request):
    # Handle order confirmation logic here
    return render(request, 'shopciti_app/order_confirmation.html')

def payfast_notify(request):
    # Your view logic here
    return HttpResponse("PayFast notification received.")

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



def checkout(request):
    cart = request.session.get('cart', {})

    total_amount = sum(item['price'] * item['quantity'] for item in cart.values())
    item_names = [f"{item['name']} - ${item['price']} x {item['quantity']}" for item in cart.values()]
    item_name = ', '.join(item_names)

    context = {
        'cart_items': cart.values(),
        'total_amount': total_amount,
        'item_name': item_name,  # Include the item_name in the context
    }

    return render(request, 'shopciti_app/checkout.html', context)


def payfast_return(request):
    # Handle order confirmation and processing here
    # You can access PayFast parameters in the request.GET dictionary

    # Example:
    payfast_data = request.GET
    # Extract and process PayFast response data

    return render(request, 'shopciti_app/order_confirmation.html')


def thank_you(request):
    return render(request, 'shopciti_app/thank_you.html')


