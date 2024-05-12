from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseServerError, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .forms import SellerApplicationForm, ProductForm, BuyerRegistrationForm
from .models import CustomUser, Product, Product, RelatedProduct, ProductVariant, Category, CartItem
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.core.files.storage import default_storage
from .forms import BillingAddressForm, VendorRegistrationForm
from django.utils.text import slugify






# View for the index page
def index(request):
    products = Product.objects.all()
    users = CustomUser.objects.exclude(is_buyer=True)

    on_sale_products = Product.objects.filter(on_sale=True)

    context = {'users': users,'products': products, 'on_sale_products': on_sale_products}

    return render(request, 'index.html', context)

# View for displaying all shops
def shops(request):
    User = get_user_model()

    if request.method == 'POST':
        form = VendorRegistrationForm(request.POST, request.FILES)

        if form.is_valid():
            # Clear session data related to previous user
            auth_logout(request)
            request.session.flush()

            # Clear initial data to ensure a new, empty form for new registrations
            form.initial = {}
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password1"])
            user.save()

            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
            if user is not None:
                login(request, user)

                # Redirect to dashboard after successful registration
                return redirect('dashboard')
        else:
            # Debugging: Print form errors to console
            print(form.errors)
    else:
        form = VendorRegistrationForm()

    # Debugging: Print request.FILES to console
    print(request.FILES)

    # Fetching all users for sidebar excluding those marked as buyers and users who are not sellers
    sidebar_users = User.objects.exclude(is_buyer=True)

    # Pagination for main content including users who haven't been marked as buyers and users who are not sellers
    users_list = User.objects.exclude(is_buyer=True)
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

    context = {'users': users, 'sidebar_users': sidebar_users, 'form': form}
    return render(request, 'shops.html', context)




# View for displaying shop information
def shop_info(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    products = Product.objects.filter(added_by=user)
    context = {'user': user, 'products': products}
    return render(request, 'shop_info.html', context)



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


# View for displaying checkout
@login_required
def checkout(request):
    if request.method == 'POST':
        # If the request is a POST request, process the billing address form
        billing_form = BillingAddressForm(request.POST)
        if billing_form.is_valid():
            billing_address = billing_form.save(commit=False)
            billing_address.user = request.user
            billing_address.save()
            # Process the rest of the checkout logic if needed
            # Redirect to a success page or another step in the checkout process
            return redirect('checkout_success')
    else:
        # If the request is not a POST request, render the checkout page with the form
        billing_form = BillingAddressForm()

    cart = request.session.get('cart', {})
    total_amount = sum(item['price'] * item['quantity'] for item in cart.values())
    item_names = [f"{item['name']}" for item in cart.values()]

    context = {
        'cart_items': cart.values(),
        'total_price': total_amount,
        'item_name': item_names,
        'billing_form': billing_form,  # Pass the billing form to the template
    }

    return render(request, 'checkout.html', context)




# View for displaying comparison
def compaire(request):
    return render(request, 'compaire.html')

# View for displaying contact us page
def contact_us(request):
    return render(request, 'contact_us.html')




def random_create_account(request):
    if request.method == 'POST':
        form = BuyerRegistrationForm(request.POST)

        if form.is_valid():
            # Clear session data related to previous user
            auth_logout(request)
            request.session.flush()

            # Generate a unique username by appending first name and last name
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = slugify(first_name + last_name)
            
            # Check if the generated username already exists
            suffix = 1
            while CustomUser.objects.filter(username=username).exists():
                username = slugify(first_name + last_name) + str(suffix)
                suffix += 1

            # Clear initial data to ensure a new, empty form for new registrations
            form.initial = {}
            random_user = form.save(commit=False)
            random_user.username = username  # Assign the generated username
            random_user.set_password(form.cleaned_data["password1"])
            
            # Mark the user as a buyer
            random_user.is_buyer = True
            
            random_user.save()

            random_user = authenticate(username=username, password=form.cleaned_data['password1'])
            if random_user is not None:
                login(request, random_user)

                # Redirect to dashboard after successful registration
                return redirect('dashboard')
        else:
            # Debugging: Print form errors to console
            print(form.errors)
    else:
        form = BuyerRegistrationForm()

    # Initialize an empty PasswordChangeForm to avoid validation errors during registration
    password_change_form = None

    return render(request, 'random_create_account.html', {'form': form, 'password_change_form': password_change_form})




def generate_unique_username(first_name, last_name):
    # Combine first name and last name and slugify to create a username
    username = slugify(first_name + last_name)
    
    # Check if the username already exists, if so, append a number to make it unique
    User = get_user_model()
    num = 1
    while User.objects.filter(username=username).exists():
        username = f"{slugify(first_name + last_name)}_{num}"
        num += 1

    return username


def create_account(request):
    if request.method == 'POST':
        form = VendorRegistrationForm(request.POST, request.FILES)

        if form.is_valid():
            # Clear session data related to previous user
            auth_logout(request)
            request.session.flush()

            # Clear initial data to ensure a new, empty form for new registrations
            form.initial = {}
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password1"])
            user.save()

            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
            if user is not None:
                login(request, user)

                # Redirect to dashboard after successful registration
                return redirect('dashboard')
        else:
            # Debugging: Print form errors to console
            print(form.errors)
    else:
        form = VendorRegistrationForm()

    # Debugging: Print request.FILES to console
    print(request.FILES)

    # Initialize an empty PasswordChangeForm to avoid validation errors during registration
    password_change_form = None

    return render(request, 'create_account.html', {'form': form, 'password_change_form': password_change_form})




@require_POST
def clear_cart(request):
    # Check if the user is authenticated
    if request.user.is_authenticated:
        # Clear the cart items associated with the current user
        CartItem.objects.filter(user=request.user).delete()
    else:
        # Clear the cart items stored in the session for anonymous users
        request.session.pop('cart', None)
    
    # Redirect back to the page the user was on
    return redirect(request.POST.get('next', '/'))


@require_POST
def remove_from_cart(request):
    product_id = request.POST.get('product_id')
    if product_id:
        # Check if the user is authenticated
        if request.user.is_authenticated:
            # Remove the specified product from the cart for the current user
            CartItem.objects.filter(user=request.user, product_id=product_id).delete()
        else:
            # Remove the specified product from the cart stored in the session for anonymous users
            cart = request.session.get('cart', {})
            if product_id in cart:
                del cart[product_id]
                request.session['cart'] = cart
    
    # Redirect back to the page the user was on
    return redirect(request.POST.get('next', '/'))


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
    product = Product.objects.get(pk=product_id)
    available_products_count = product.available_quantity
    context = {'product': product, 'available_products_count': available_products_count}
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

    total_quantity = sum(item['quantity'] for item in cart.values())
    total_price = sum(float(item['price']) * item['quantity'] for item in cart.values())

    # Return JSON response with updated total quantity and price
    return JsonResponse({'total_quantity': total_quantity, 'total_price': total_price})


@login_required
def cart(request):
    cart = request.session.get('cart', {})  # Default to empty dictionary if cart is not found
    cart_items = cart.values()
    total_quantity = sum(item['quantity'] for item in cart_items)
    total_price = sum(float(item['price']) * item['quantity'] for item in cart_items)

    # Convert cart_items to a list of dictionaries for easier processing in JavaScript
    cart_items_list = list(cart_items)

    return render(request, 'cart.html', {'cart_items': cart_items_list, 'total_quantity': total_quantity, 'total_price': total_price})


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
        user = request.user
        user = get_object_or_404(CustomUser, username=request.user.username)
        products = Product.objects.filter(added_by=request.user)

        if request.method == 'POST':
            user.first_name = request.POST.get('first_name', '')
            user.last_name = request.POST.get('last_name', '')
            user.email = request.POST.get('email', '')
            user.phone_number = request.POST.get('phone_number', '')
            user.country = request.POST.get('country', '')
            user.address = request.POST.get('address', '')
            user.city = request.POST.get('city', '')
            user.postal_code = request.POST.get('postal_code', '')


            # Handle logo upload
            logo_file = request.FILES.get('logo')
            if logo_file:
                # Save the uploaded logo
                file_path = default_storage.save(logo_file.name, logo_file)
                user.logo = file_path

            # Check if the password change form data is present
            if 'old_password' in request.POST and 'new_password1' in request.POST and 'new_password2' in request.POST:
                password_change_form = PasswordChangeForm(user, request.POST)
                if password_change_form.is_valid():
                    password_change_form.save()
                    update_session_auth_hash(request, user)  # Update the user's session to prevent them from being logged out
                    messages.success(request, 'Password updated successfully!')
                else:
                    messages.error(request, 'Please correct the error below.')

            user.save()

            messages.success(request, 'Profile updated successfully!')
            return redirect('dashboard')  # Redirect to prevent form resubmission
        else:
            password_change_form = PasswordChangeForm(request.user)

        return render(request, 'dashboard.html', {'products': products, 'password_change_form': password_change_form})
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
            available_quantity = request.POST.get('available_quantity')  # Get the available quantity from the form
            if available_quantity is not None and int(available_quantity) >= 1:
                product.available = int(available_quantity)
            else:
                product.available = True  # Set availability to True if available quantity is provided and greater than 0
            product.save()
            form.save_m2m()  # Save many-to-many relationships (categories)
            return redirect('dashboard')  # Redirect to dashboard after adding a product
    else:
        form = ProductForm()
    
    categories = Category.objects.all()  # Retrieve all categories from the database
    context = {'form': form, 'categories': categories}  # Pass form and categories to the template

    return render(request, 'add_product.html', context)



# Function to fetch related products for a given product
def get_related_products(product_id):
    product = Product.objects.get(pk=product_id)
    related_products = RelatedProduct.objects.filter(main_product=product)
    return related_products

# Function to fetch product variants for a given product
def get_product_variants(product_id):
    product = Product.objects.get(pk=product_id)
    variants = ProductVariant.objects.filter(product=product)
    return variants

# Function to fetch product variants with size and color for a given product
def get_product_variants_with_details(product_id):
    product = Product.objects.get(pk=product_id)
    variants_with_details = ProductVariant.objects.filter(product=product).select_related('product')
    return variants_with_details

# Function to fetch related products with details for a given product
def get_related_product_details(product_id):
    product = Product.objects.get(pk=product_id)
    related_products_with_details = RelatedProduct.objects.filter(main_product=product).select_related('related_product__product')
    return related_products_with_details

# View for displaying product information
def product_info(request, product_id):
    product = Product.objects.get(pk=product_id)
    related_products = get_related_products(product_id)
    variants = get_product_variants(product_id)
    available_products_count = product.available if product.available is not None else 0
    categories = Category.objects.all()  # Retrieve all categories from the database    
    context = {
        'product': product,
        'available_products_count': available_products_count,
        'related_products': related_products,
        'variants': variants,
        'categories': categories
    }
    return render(request, 'product_info.html', context)

def payfast_return(request):
    # Handle order confirmation and processing here
    # You can access PayFast parameters in the request.GET dictionary

    # Example:
    payfast_data = request.GET
    # Extract and process PayFast response data

    return render(request, 'shopciti_app/order_confirmation.html')

def payfast_notify(request):
    # Your view logic here
    return HttpResponse("PayFast notification received.")

