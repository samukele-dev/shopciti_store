from .models import Product
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
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
from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from django.urls import reverse



def about(request):
    return render(request, 'about.html')


def become_vendor(request):
    return render(request, 'become_vendor.html')


def blogs_details(request):
    return render(request, 'blogs_details.html')

def blogs(request):
    return render(request, 'blogs.html')

def cart(request):
    return render(request, 'cart.html')

def checkout(request):
    return render(request, 'checkout.html')

def compaire(request):
    return render(request, 'compaire.html')


def contact_us(request):
    return render(request, 'contact_us.html')

def create_account(request):
    return render(request, 'create_account.html')

def empty_cart(request):
    return render(request, 'empty_cart.html')

def empty_wishlist(request):
    return render(request, 'empty_wishlist.html')

def faq(request):
    return render(request, 'faq.html')

def flash_sale(request):
    return render(request, 'flash_sale.html')

def blogs_details(request):
    return render(request, 'blogs_details.html')

def flash(request):
    return render(request, 'flash.html')

def index(request):
    return render(request, 'index.html')

def login(request):
    return render(request, 'login.html')

def order(request):
    return render(request, 'order.html')

def privacy(request):
    return render(request, 'privacy.html')


def product_info(request):
    return render(request, 'product_info.html')


def product_sidebar(request):
    return render(request, 'product_sidebar.html')


def seller_sidebar(request):
    return render(request, 'seller_sidebar.html')

def sellers(request):
    return render(request, 'sellers.html')


def terms(request):
    return render(request, 'terms.html')

def user_profile(request):
    return render(request, 'user_profile.html')

def wishlist(request):
    return render(request, 'wishlist.html')

# /////////////////////////////////////////////////////////

class SupplierLoginView(LoginView):
    template_name = 'shopciti_app/login.html'

class UserLoginView(LoginView):
    template_name = 'shopciti_app/login_user.html'

    def get_success_url(self):
        # Get the 'next' parameter from the request
        next_url = self.request.GET.get('next')
        
        # Check if the 'next' parameter is a valid URL
        if next_url and self.request.build_absolute_uri(next_url) == next_url:
            return next_url
        else:
            # Redirect to a default URL if 'next' is not a valid URL
            return '/'

    def form_valid(self, form):
        # Call the parent class's form_valid method, which performs the login
        response = super().form_valid(form)

        # Redirect to the URL obtained from get_success_url
        return HttpResponseRedirect(self.get_success_url())

# You can also create similar custom views for logout if needed
class SupplierLogoutView(LogoutView):
    pass

class UserLogoutView(LogoutView):
    pass


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('register_store')  # Redirect to the user's profile page
    else:
        form = CustomUserCreationForm()
    return render(request, 'shopciti_app/register.html', {'form': form})

def register_user(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('account_user_info')  # Redirect to the user's profile page
    else:
        form = CustomUserCreationForm()
    return render(request, 'shopciti_app/register_user.html', {'form': form})


def product_list(request):
    products = Product.objects.all()
    return render(request, 'shopciti_app/product_list.html', {'products': products})

def home2(request):
    return render(request, 'shopciti_app/home2.html')

def home1(request):
    return render(request, 'shopciti_app/home1.html')

@login_required
def user_profile(request):
    user = request.user

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user)

        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully.')

    else:
        form = UserProfileForm(instance=user)

    try:
        store = user.store
    except ObjectDoesNotExist:
        store = None

    try:
        store_profile = StoreProfile.objects.get(store=store)
    except ObjectDoesNotExist:
        store_profile = None

    profile_image_url = None
    if user.profile_image and user.profile_image.url:
        profile_image_url = user.profile_image.url

    return render(request, 'shopciti_app/store_profile.html', {
        'user': user,
        'store': store,
        'store_profile': store_profile,
        'profile_image_url': profile_image_url,
        'form': form,
    })

def account_user_info(request):
    return render(request, 'shopciti_app/account_user_info.html')

def user_orders(request):
    return render(request, 'shopciti_app/user_orders.html')


@login_required
def edit_profile(request):
    user = request.user
    store_name = None  # Default value for store_name

    # Check if the user has an associated store
    if hasattr(user, 'store'):
        store = user.store
        subscription_level = store.subscription_level
        store_name = store.name  # Assign store name if available

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user)

        if form.is_valid():
            form.save()

            # Update store name if present in the form data
            if 'store_name' in request.POST:
                store_name = request.POST['store_name']
                if hasattr(user, 'store'):
                    user.store.name = store_name
                    user.store.save()

            messages.success(request, 'Your profile has been updated successfully.')
            return redirect('user_profile')

    else:
        form = UserProfileForm(instance=user)

    return render(request, 'shopciti_app/edit_profile.html', {'form': form, 'subscription_level': subscription_level, 'store_name': store_name})



@login_required
def register_store(request):
    user = request.user
    subscription_level = "free"
    
    if hasattr(user, 'profile'):
        subscription_level = user.profile.subscription_level

    if request.method == 'POST':
        form = StoreForm(request.POST, request.FILES)
        if form.is_valid():
            new_store = form.save()
            user.store = new_store
            user.save()

            if subscription_level == "free":
                return render(request, 'shopciti_app/store_profile_free.html')
            else:
                return render(request, 'shopciti_app/store_profile.html')

    else:
        form = StoreForm()

    return render(request, 'shopciti_app/register_store.html', {'form': form, 'subscription_level': subscription_level})


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


def shop_detail(request, shop_id):
    shop = get_object_or_404(Store, pk=shop_id)
    products = Product.objects.filter(store=shop)
    return render(request, 'shopciti_app/shop_detail.html', {'shop': shop, 'products': products})


def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return render(request, 'shopciti_app/product_detail.html', {'product': product})

@login_required
def store_profile(request):
    user = request.user
    try:
        store = user.store
    except ObjectDoesNotExist:
        # Handle the case where the custom user or store does not exist
        return redirect('registration_failure')

    try:
        store_profile = StoreProfile.objects.get(store=store)
    except ObjectDoesNotExist:
        # Handle the case where the store profile does not exist
        store_profile = None

    subscription_level = store.subscription_level

    if request.method == 'POST':
        # Handle form submission and save changes here
        # For example, you can update the user's profile
        user.username = request.POST.get('username')
        user.email = request.POST.get('email')
        user.save()

        # Update the subscription level if it's available in the request
        new_subscription_level = request.POST.get('subscription')
        if new_subscription_level and new_subscription_level in [choice[0] for choice in Store.SUBSCRIPTION_CHOICES]:
            store.subscription_level = new_subscription_level
            store.save()

        # After processing the form, redirect to the store_profile page
        return redirect('store_profile')

    
    context = {
        'store': store,
        'store_profile': store_profile,
        'subscription_level': subscription_level,
    }

    return render(request, 'shopciti_app/store_profile.html', context)



@login_required
def store_profile_free(request):
    user = request.user
    try:
        store = user.store
    except ObjectDoesNotExist:
        # Handle the case where the custom user or store does not exist
        return redirect('registration_failure')

    try:
        store_profile = StoreProfile.objects.get(store=store)
    except ObjectDoesNotExist:
        # Handle the case where the store profile does not exist
        store_profile = None

    subscription_level = store.subscription_level
    
    context = {
        'store': store,
        'store_profile': store_profile,
        'subscription_level': subscription_level,
    }

    return render(request, 'shopciti_app/store_profile.html', context)


def product_list(request):
    products = Product.objects.all()
    return render(request, 'shopciti_app/product_list.html', {'products': products})

def calculate_total_price(cart):
    total_price = sum(item['price'] * item['quantity'] for item in cart.values())
    return total_price

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

    # Calculate the total cart quantity
    total_quantity = sum(item['quantity'] for item in cart.values())

    # Calculate the total cart price
    total_price = calculate_total_price(cart)

    # Return JSON response with updated cart data
    response_data = {
        'quantity': total_quantity,
        'cart_items': list(cart.values()),
        'total_price': total_price,
    }

    return JsonResponse(response_data)


# Remove a product from the cart
def remove_from_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = Cart(request)
    cart.remove(product)
    return redirect('cart')




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
        'item_name': item_name,
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


