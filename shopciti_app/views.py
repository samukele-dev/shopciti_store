from django.urls import reverse
from django.contrib.auth import login
from django.shortcuts import render, redirect, get_object_or_404




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
