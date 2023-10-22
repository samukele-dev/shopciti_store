from django.urls import reverse
from .models import Product


def remove_from_cart_url(product_id):
    return reverse('remove_from_cart', args=[product_id])

def update_cart_url(product_id):
    return reverse('update_cart', args=[product_id])

def cart_context(request):
    # Fetch the cart data and calculate the total price
    cart = request.session.get('cart', {})
    cart_items = cart.values()
    total_price = sum(item['price'] * item['quantity'] for item in cart.values())
    item_names = [f"{item['name']} - ${item['price']} x {item['quantity']}" for item in cart.values()]
    item_name = ', '.join(item_names)  # Comma-separated list of item names


    return {
        'cart_items': cart_items,
        'total_price': total_price,
        'item_name': item_name,
        'remove_from_cart_url': remove_from_cart_url,  # Function to generate "Remove" URL
        'update_cart_url': update_cart_url,  # Function to generate "Update Cart" URL
    }

def cart(request):
    cart = request.session.get('cart', {})
    total_quantity = sum(item['quantity'] for item in cart.values())
    return {'quantity': total_quantity}