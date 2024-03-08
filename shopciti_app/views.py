# views.py

from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseServerError
from django.shortcuts import render, redirect, get_object_or_404
from .forms import CustomUserCreationForm, SellerApplicationForm, ProductForm
from .models import CustomUser, Product, CartItem
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import json


# View for the index page
def index(request):
    products = Product.objects.all()
    context = {'products': products}

    return render(request, 'index.html', context)

# View for displaying all shops
def shops(request):
    # Fetching all users for sidebar
    sidebar_users = CustomUser.objects.all()

    # Pagination for main content
    users_list = CustomUser.objects.all()
    paginator = Paginator(users_list, 10)  # Show 10 users per page

    page = request.GET.get('page')
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        users = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        users = paginator.page(paginator.num_pages)

    context = {'users': users, 'sidebar_users': sidebar_users}
    return render(request, 'shops.html', context)


# View for displaying shop information
def shop_info(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    products = Product.objects.filter(added_by=user)
    context = {'user': user, 'products': products}
    return render(request, 'shop_info.html', context)

# View for user login
def custom_login(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        return LoginView.as_view(template_name='login.html')(request)

# View for user logout
def custom_logout(request):
    return LogoutView.as_view()(request)

# View for displaying about page
def about(request):
    return render(request, 'about.html')

# View for vendor registration
def become_vendor(request):
    if request.method == 'POST':
        form = SellerApplicationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success-page')  # Redirect to success page after vendor registration
    else:
        form = SellerApplicationForm()
    return render(request, 'become_vendor.html', {'form': form})

# View for displaying blog details
def blogs_details(request):
    return render(request, 'blogs_details.html')

# View for displaying blogs
def blogs(request):
    return render(request, 'blogs.html')

# View for displaying cart
def cart(request):
    return render(request, 'cart.html')

# View for displaying checkout
def checkout(request):
    return render(request, 'checkout.html')

# View for displaying comparison
def compaire(request):
    return render(request, 'compaire.html')

# View for displaying contact us page
def contact_us(request):
    return render(request, 'contact_us.html')

# View for user registration
def create_account(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
            if user is not None:
                login(request, user)
                return redirect('dashboard')  # Redirect to dashboard after successful registration
    else:
        form = CustomUserCreationForm()
    return render(request, 'create_account.html', {'form': form})

# View for displaying empty cart page
def empty_cart(request):
    return render(request, 'empty_cart.html')

# View for displaying empty wishlist page
def empty_wishlist(request):
    return render(request, 'empty_wishlist.html')

# View for frequently asked questions page
def faq(request):
    return render(request, 'faq.html')

# View for displaying flash sale page
def flash_sale(request):
    return render(request, 'flash_sale.html')

# View for displaying privacy policy page
def privacy(request):
    return render(request, 'privacy.html')

# View for displaying product information
def product_info(request, product_id):

    # Retrieve the product based on the product_id
    product = get_object_or_404(Product, pk=product_id)
    context = {'product': product}
    return render(request, 'product_info.html', context)

# View for displaying product sidebar
def product_sidebar(request):
    sidebar_users = CustomUser.objects.all()

    products = Product.objects.all()

    # Pagination for main content
    users_list = CustomUser.objects.all()
    paginator = Paginator(users_list, 10)  # Show 10 users per page

    page = request.GET.get('page')
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        users = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        users = paginator.page(paginator.num_pages)


    # Pagination for main content
    context = {'products': products, 'sidebar_users': sidebar_users, 'users': users}

    return render(request, 'product_sidebar.html', context)

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
            'price': float(product.price),  # Convert Decimal to float
            'quantity': 1,
        }

    cart[str(product_id)] = cart_item
    request.session['cart'] = cart
    return redirect('cart')



def cart(request):
    cart = request.session.get('cart', {})  # Default to empty dictionary if cart is not found
    cart_items = cart.values()
    total_price = sum(float(item['price']) * item['quantity'] for item in cart_items)
    return render(request, 'shopciti_app/cart.html', {'cart_items': cart_items, 'total_price': total_price})



# View for displaying seller sidebar
def seller_sidebar(request):
    return render(request, 'seller_sidebar.html')

# View for displaying sellers page
def sellers(request):
    return render(request, 'sellers.html')

# View for displaying terms and conditions page
def terms(request):
    return render(request, 'terms.html')

# View for dashboard (requires login)
@login_required
def dashboard(request):
    try:
        user = get_object_or_404(CustomUser, username=request.user.username)
        products = Product.objects.filter(added_by=request.user)
        context = {'products': products}
        return render(request, 'dashboard.html', context)
    except Exception as e:
        print("An error occurred:", e)
        return HttpResponseServerError("An error occurred. Please try again later.")

# View for displaying wishlist page
def wishlist(request):
    return render(request, 'wishlist.html')

# View for adding a product (requires login)
@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.added_by = request.user
            product.save()
            return redirect('dashboard')  # Redirect to dashboard after adding a product
    else:
        form = ProductForm()
    return render(request, 'add_product.html', {'form': form})
