from django.urls import reverse


def remove_from_cart_url(product_id):
    return reverse('remove_from_cart', args=[product_id])

def update_cart_url(product_id):
    return reverse('update_cart', args=[product_id])


def cart(request):
    cart = request.session.get('cart', {})
    cart_items = cart.values()
    total_quantity = sum(item['quantity'] for item in cart_items)
    return {'total_quantity': total_quantity}