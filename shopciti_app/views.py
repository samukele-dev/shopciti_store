from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.views import LogoutView
from django.http import HttpResponseServerError, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .forms import SellerApplicationForm, ProductForm, BuyerRegistrationForm, SupportTicketForm, PaymentMethodForm
from .models import CustomUser, Product, Product, RelatedProduct, ProductVariant, Category, CartItem, Cart, SupportTicket, PaymentMethod, Order, OrderItem, Size
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.core.files.storage import default_storage
from .forms import BillingAddressForm, VendorRegistrationForm
from django.utils.text import slugify
from django.db.models import Sum, F
from django.contrib.auth.decorators import user_passes_test
from django.urls import reverse
import uuid
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from hashlib import md5
from django.conf import settings


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

class CustomLoginView(auth_views.LoginView):
    template_name = 'login.html'

    def form_valid(self, form):
        # Call the parent class form_valid method
        super().form_valid(form)

        # Check if the logged-in user is authenticated and is a buyer
        if self.request.user.is_authenticated:
            if self.request.user.is_buyer:  # Assuming is_buyer is a field on your user model
                return redirect('random_user_dashboard')  # Redirect to buyer's dashboard
            else:
                return redirect('dashboard')  # Redirect to vendor's or another type's dashboard

        # Default to login page if conditions are not met
        return redirect(reverse_lazy('login'))


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

# View for displaying comparison
def compaire(request):
    return render(request, 'compaire.html')

# View for displaying contact us page
def contact_us(request):
    return render(request, 'contact_us.html')

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

def random_create_account(request):
    # Check if there's a stored next URL in the session
    next_url = request.session.get('next_url', None)
    
    if request.method == 'POST':
        form = BuyerRegistrationForm(request.POST)

        if form.is_valid():
            # Clear session data related to previous user
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

            # Save the user with the generated username and hashed password
            random_user = form.save(commit=False)
            random_user.username = username
            random_user.set_password(form.cleaned_data["password1"])
            random_user.is_buyer = True  # Mark the user as a buyer
            random_user.save()

            # Authenticate and login the user
            random_user = authenticate(username=username, password=form.cleaned_data['password1'])
            if random_user is not None:
                login(request, random_user)
                if next_url:
                    return redirect(next_url)
                else:
                    return redirect('random_user_dashboard')
        else:
            # Debugging: Print form errors to console
            print(form.errors)
    else:
        form = BuyerRegistrationForm()

        # Store the current URL in session to redirect back after registration
        request.session['next_url'] = request.GET.get('next', None)

    # Initialize an empty PasswordChangeForm to avoid validation errors during registration
    password_change_form = PasswordChangeForm(user=request.user) if request.user.is_authenticated else None

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

@login_required
def cart_total_quantity(request):
    total_quantity = CartItem.objects.filter(user=request.user).aggregate(total=Sum('quantity'))['total'] or 0
    return JsonResponse({'total_quantity': total_quantity})

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

    # Calculate the updated total quantity and price for the current user
    total_quantity = CartItem.objects.filter(user=request.user).aggregate(total=Sum('quantity'))['total'] or 0
    total_price = CartItem.objects.filter(user=request.user).aggregate(total=Sum(F('quantity') * F('product__price')))['total'] or 0

    # Redirect to the cart page (or any other page you want)
    return redirect('cart')  # Replace 'cart_page' with your cart page URL name

@require_POST
def clear_cart(request):
    # Check if the user is authenticated
    if request.user.is_authenticated:
        clear_user_cart(request.user)
    else:
        clear_session_cart(request.session)

    # Redirect to the cart page (or any other page you want)
    return redirect('cart')  # Replace 'cart_page' with your cart page URL name

# View for frequently asked questions page
def faq(request):
    return render(request, 'faq.html')

# View for displaying flash sale page
def flash_sale(request):
    return render(request, 'flash_sale.html')

# View for displaying privacy policy page
def privacy(request):
    return render(request, 'privacy.html')



# View for displaying product sidebar
def product_sidebar(request):
    User = get_user_model()

    sidebar_users = User.objects.exclude(is_buyer=True)

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

# Function to generate order ID
def generate_order_id():
    prefix = 'ORD'
    unique_id = uuid.uuid4().hex[:8].upper()  # Generate a random UUID and take first 8 characters
    order_id = f"{prefix}-{unique_id}"
    return order_id

@login_required
def cart(request):
    user = request.user
    cart = get_object_or_404(Cart, user=user)
    cart_items = CartItem.objects.filter(cart=cart)

    total_quantity = sum(item.quantity for item in cart_items)
    total_price = sum(item.get_total_price() for item in cart_items)

    if request.method == 'POST' and 'checkout' in request.POST:
        if not cart.order_id:
            cart.order_id = generate_order_id()  # Generate order ID if it doesn't exist
            cart.save()
            print(f"Order ID set in cart view: {cart.order_id}")  # Debug statement

        return redirect('checkout', order_id=cart.order_id)  # Redirect with order_id

    context = {
        'cart_items': cart_items,
        'total_quantity': total_quantity,
        'total_price': total_price,
        'order_id': cart.order_id,  # Pass order_id to the template context
    }

    print(f"Order ID before rendering in cart view: {cart.order_id}")  # Debug statement
    return render(request, 'cart.html', context)

# View for displaying checkout
@login_required
def checkout(request, order_id=None):
    user = request.user
    cart = Cart.objects.filter(user=user).first()
    cart_items = CartItem.objects.filter(cart=cart) if cart else []

    if not order_id and cart:
        order_id = generate_order_id()  # Generate order ID if not provided

    if request.method == 'POST':
        billing_form = BillingAddressForm(request.POST)
        if billing_form.is_valid():
            billing_address = billing_form.save(commit=False)
            billing_address.user = request.user
            billing_address.save()

            total_price = sum(item.product.price * item.quantity for item in cart_items)

            # Create order instance with retrieved order_id
            order = Order.objects.create(order_id=order_id, user=user, total_price=total_price)

            # Create order items
            for item in cart_items:
                OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity)

            # Clear cart items
            cart_items.delete()

            # Redirect to checkout success page or other appropriate action
            return redirect('checkout_success')  # Replace with your success URL
    else:
        billing_form = BillingAddressForm()

    # Calculate total_price and item_names
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    item_names = [item.product.name for item in cart_items]

    context = {
        'cart_items': cart_items,
        'billing_form': billing_form,
        'total_price': total_price,
        'item_names': item_names,
        'order_id': order_id,
    }

    return render(request, 'checkout.html', context)


def login_required_to_random_create_account(view_func):
    @user_passes_test(lambda u: u.is_authenticated, login_url='/random_create_account/')
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            # Store the current path in session
            request.session['redirect_to'] = request.path
            return redirect(reverse('random_create_account'))
        return view_func(request, *args, **kwargs)
    return wrapper


@login_required_to_random_create_account
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    user = request.user

    # Check if the user has a cart, if not create one
    cart, _ = Cart.objects.get_or_create(user=user)

    # Add the product to the user's cart
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product, user=user)
    if not created:
        # If the item already exists in the cart, increase its quantity
        cart_item.quantity += 1
    cart_item.save()

    # Calculate total quantity and total price
    total_quantity = sum(item.quantity for item in CartItem.objects.filter(cart=cart))
    total_price = sum(item.product.price * item.quantity for item in CartItem.objects.filter(cart=cart))

    return JsonResponse({'total_quantity': total_quantity, 'total_price': total_price})


def clear_user_cart(user):
    CartItem.objects.filter(user=user).delete()

def clear_session_cart(session):
    session.pop('cart', None)

def validate_payfast_data(data):
    # Extract relevant data from the PayFast notification
    merchant_id = data.get('merchant_id')
    order_id = data.get('m_payment_id')
    payment_status = data.get('payment_status')
    pf_payment_id = data.get('pf_payment_id')
    signature = data.get('signature')

    # Generate the signature for verification
    generated_signature = generate_signature(data)

    # Verify the signature
    if signature == generated_signature:
        # Signature is valid, now verify other details
        if merchant_id == settings.PAYFAST_MERCHANT_ID:  # Replace with your actual PayFast merchant ID
            # Check payment status for successful transaction
            if payment_status.lower() == 'completed':
                return True
    return False

def generate_signature(data):
    # Construct the signature string based on PayFast documentation
    # Use the secret key provided by PayFast (stored securely in your settings)
    signature_string = '&'.join([
        f"{key}={value}" for key, value in sorted(data.items()) if key != 'signature'
    ])
    signature_string += f"&passphrase={settings.PAYFAST_PASSPHRASE}"  # Add passphrase

    # Generate MD5 hash of the signature string
    generated_signature = md5(signature_string.encode()).hexdigest()

    return generated_signature

@csrf_exempt
def payfast_notify(request):
    if request.method == 'POST':
        data = request.POST

        # Validate the data with PayFast (example assumes a function validate_payfast_data exists)
        if validate_payfast_data(data):
            order_id = data.get('m_payment_id')
            payment_status = data.get('payment_status')

            try:
                order = Order.objects.get(order_id=order_id)
                order.payment_status = payment_status
                order.save()

                # Clear the user's cart
                clear_user_cart(order.user)

                # Redirect to the appropriate dashboard
                if order.user.is_buyer:  # Assuming is_buyer is a field on your user model
                    return redirect('random_user_dashboard')  # Redirect to buyer's dashboard
                else:
                    return redirect('dashboard')  # Redirect to vendor's or another type's dashboard

            except Order.DoesNotExist:
                # Create a new order if it does not exist
                order = Order.objects.create(
                    user=request.user,
                    order_id=order_id,
                    payment_status=payment_status
                )

                # Get the cart items
                cart_items = CartItem.objects.filter(user=request.user)

                # Save order items
                for item in cart_items:
                    OrderItem.objects.create(
                        order=order,
                        product=item.product,  # Assuming CartItem has a foreign key to Product
                        quantity=item.quantity,
                        price=item.product.price
                    )

                # Clear the user's cart
                clear_user_cart(order.user)

                # Redirect to the appropriate dashboard
                if order.user.is_buyer:
                    return redirect('random_user_dashboard')
                else:
                    return redirect('dashboard')

    return HttpResponse("Invalid request", status=400)


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
        support_tickets = SupportTicket.objects.filter(user=request.user).order_by('-created_at')
        payment_methods = PaymentMethod.objects.filter(user=request.user).order_by('-created_at')

        password_change_form = PasswordChangeForm(request.user)
        ticket_form = SupportTicketForm()
        payment_method_form = PaymentMethodForm()

        if request.method == 'POST':
            if 'first_name' in request.POST and 'last_name' in request.POST:
                # Handle profile update form
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

                user.save()
                messages.success(request, 'Profile updated successfully!')
                return redirect('dashboard')

            elif 'old_password' in request.POST and 'new_password1' in request.POST and 'new_password2' in request.POST:
                # Handle password change form
                password_change_form = PasswordChangeForm(user, request.POST)
                if password_change_form.is_valid():
                    password_change_form.save()
                    update_session_auth_hash(request, user)
                    messages.success(request, 'Password updated successfully!')
                else:
                    messages.error(request, 'Please correct the error below.')
                return redirect('dashboard')

            elif 'description' in request.POST:
                # Handle support ticket form
                ticket_form = SupportTicketForm(request.POST)
                if ticket_form.is_valid():
                    support_ticket = ticket_form.save(commit=False)
                    support_ticket.user = request.user
                    support_ticket.save()
                    messages.success(request, 'Support ticket submitted successfully!')
                else:
                    messages.error(request, 'Please correct the errors in the support ticket form.')
                return redirect('dashboard')
            
            elif 'card_number' in request.POST and 'card_holder_name' in request.POST and 'expiry_date' in request.POST and 'cvv' in request.POST:
                # Handle payment method form
                payment_method_form = PaymentMethodForm(request.POST)
                if payment_method_form.is_valid():
                    payment_method = payment_method_form.save(commit=False)
                    payment_method.user = request.user
                    payment_method.save()
                    messages.success(request, 'Payment method added successfully!')
                else:
                    messages.error(request, 'Please correct the errors in the payment method form.')

        return render(request, 'dashboard.html', {
            'products': products,
            'password_change_form': password_change_form,
            'ticket_form': ticket_form,
            'support_tickets': support_tickets,
            'payment_methods': payment_methods,
            'payment_method_form': payment_method_form
        })
    except Exception as e:
        print("An error occurred:", e)
        return HttpResponseServerError("An error occurred. Please try again later.")

@login_required
def remove_product(request):
    product_id = request.POST.get('product_id')
    if product_id:
        # Check if the user is authenticated
        if request.user.is_authenticated:
            # Remove the specified product from the dashboard for the current user
            Product.objects.filter(added_by=request.user, id=product_id).delete()
        else:
            # Remove the specified product from the dashboard stored in the session for anonymous users
            dashboard_products = request.session.get('dashboard', {})
            if product_id in dashboard_products:
                del dashboard_products[product_id]
                request.session['dashboard'] = dashboard_products

    # Redirect to the dashboard page
    return redirect('dashboard')


# View for dashboard (requires login)
@login_required
def random_user_dashboard(request):
    try:
        user = request.user
        user = get_object_or_404(CustomUser, username=request.user.username)
        support_tickets = SupportTicket.objects.filter(user=request.user).order_by('-created_at')
        orders = Order.objects.filter(user=request.user).prefetch_related('items').order_by('-created_at')

        password_change_form = PasswordChangeForm(request.user)
        ticket_form = SupportTicketForm()

        if request.method == 'POST':
            if 'first_name' in request.POST and 'last_name' in request.POST:  # Handle profile update form
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

                user.save()
                messages.success(request, 'Profile updated successfully!')
                return redirect('random_user_dashboard')  # Redirect to prevent form resubmission

            elif 'old_password' in request.POST and 'new_password1' in request.POST and 'new_password2' in request.POST:  # Handle password change form
                password_change_form = PasswordChangeForm(user, request.POST)
                if password_change_form.is_valid():
                    password_change_form.save()
                    update_session_auth_hash(request, user)  # Update the user's session to prevent them from being logged out
                    messages.success(request, 'Password updated successfully!')
                else:
                    messages.error(request, 'Please correct the error below.')
                return redirect('random_user_dashboard')

            elif 'description' in request.POST:  # Handle support ticket form
                ticket_form = SupportTicketForm(request.POST)
                if ticket_form.is_valid():
                    support_ticket = ticket_form.save(commit=False)
                    support_ticket.user = request.user
                    support_ticket.save()
                    messages.success(request, 'Support ticket submitted successfully!')
                else:
                    messages.error(request, 'Please correct the errors in the support ticket form.')
                return redirect('random_user_dashboard')

        return render(request, 'random_user_dashboard.html', {
            'password_change_form': password_change_form,
            'ticket_form': ticket_form,
            'support_tickets': support_tickets,
            'orders': orders,
        })
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
            
            # Handle available quantity
            available = request.POST.get('available_quantity')
            if available is not None and int(available) >= 1:
                product.available = int(available)
            else:
                product.available = 0
            
            product.save()
            form.save_m2m()  # Save many-to-many relationships (categories)

            # Process sizes
            selected_sizes = request.POST.getlist('sizes')
            product.sizes.clear()  # Clear existing sizes
            for size_id in selected_sizes:
                size = Size.objects.get(id=size_id)
                product.sizes.add(size)

            return redirect('dashboard')
    else:
        form = ProductForm()

    categories = Category.objects.all()
    sizes = Size.objects.all()
    context = {'form': form, 'categories': categories, 'sizes': sizes}
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
def product_info(request, product_id, user_id=None):
    user = get_object_or_404(CustomUser, id=user_id) if user_id else None
    product = Product.objects.get(pk=product_id)
    products = Product.objects.filter(added_by=user)
    sizes = product.sizes.all()  # Retrieve all sizes associated with the product
    related_products = get_related_products(product_id)
    variants = get_product_variants(product_id)
    available_products_count = product.available if product.available is not None else 0
    categories = Category.objects.all()  # Retrieve all categories from the database
    
    context = {
        'user': user,
        'product': product,
        'products': products,
        'sizes': sizes,  # Pass sizes to the context
        'available_products_count': available_products_count,
        'related_products': related_products,
        'variants': variants,
        'categories': categories,
        'available_quantity': product.available  # Add available_quantity to context
    }
    return render(request, 'product_info.html', context)



def payfast_success(request):
    # Clear the user's cart
    if request.user.is_authenticated:
        Cart.objects.filter(user=request.user).delete()
    else:
        # Handle for anonymous users if necessary
        pass

    # Save the purchased items or create an order record if needed
    # Example: Saving items to order history
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(cart__user=request.user)
        for item in cart_items:
            Order.objects.create(
                user=request.user,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )

    # Provide feedback to the user
    messages.success(request, 'Payment successful! Your order has been placed.')

    # Redirect to the random_user_dashboard
    return redirect('random_user_dashboard')


def payfast_return(request):
    # Handle order confirmation and processing here
    # You can access PayFast parameters in the request.GET dictionary
    # Example:
    payfast_data = request.GET
    # Extract and process PayFast response data

    return render(request, 'shopciti_app/order_confirmation.html')
