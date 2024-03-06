from django.contrib.auth import views as auth_views

from django.urls import path
from . import views 


urlpatterns = [
#//////////////////////////////////////////////////////////////////
    path('', views.index, name='index'),
    path('shops/', views.shops, name='shops'),
    path('shop-info/<int:user_id>/', views.shop_info, name='shop_info'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('about/', views.about, name='about'),
    path('become-vendor/', views.become_vendor, name='become_vendor'),
    path('blogs-details/', views.blogs_details, name='blogs_details'),
    path('blogs/', views.blogs, name='blogs'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('compaire/', views.compaire, name='compaire'),
    path('contact-us/', views.contact_us, name='contact_us'),
    path('create-account/', views.create_account, name='create_account'),
    path('empty-cart/', views.empty_cart, name='empty_cart'),
    path('empty-wishlist/', views.empty_wishlist, name='empty_wishlist'),
    path('faq/', views.faq, name='faq'),
    path('flash-sale/', views.flash_sale, name='flash_sale'),
    path('privacy/', views.privacy, name='privacy'),
    path('product-info/', views.product_info, name='product_info'),
    path('product-sidebar/', views.product_sidebar, name='product_sidebar'),
    path('seller-sidebar/', views.seller_sidebar, name='seller_sidebar'),
    path('sellers/', views.sellers, name='sellers'),
    path('terms/', views.terms, name='terms'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('add-product/', views.add_product, name='add_product'),
]
