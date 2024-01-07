from django.contrib.auth import views as auth_views

from django.urls import path
from . import views 
from .views import SupplierLoginView, UserLoginView, SupplierLogoutView, UserLogoutView


urlpatterns = [
    path('', views.home1, name='home_shops'),  # Define a home view
    path('home2/', views.home2, name='home2'),
    path('products/', views.product_list, name='product_list'),
    path('register/', views.register, name='register'),
    path('register-user/', views.register_user, name='register_user'),
    # Supplier login and logout
    path('login/', SupplierLoginView.as_view(), name='login'),
    path('logout/', SupplierLogoutView.as_view(), name='logout'),

#//////////////////////////////////////////////////////////////////
    path('index/', views.index, name='index'),
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
    path('user-profile/', views.user_profile, name='user_profile'),
    path('wishlist/', views.wishlist, name='wishlist'),

    # User login and logout
    path('login-user/', UserLoginView.as_view(), name='login_user'),
    path('logout-user/', UserLogoutView.as_view(), name='logout_user'),
    path('user-profile/', views.user_profile, name='user_profile'),
    path('account-user-info/', views.account_user_info, name='account_user_info'),
    path('user-orders/', views.account_user_info, name='user_orders'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('register-store/', views.register_store, name='register_store'),
    path('registration-success/', views.registration_success, name='registration_success'),
    path('registration-failure/', views.registration_failure, name='registration_failure'),
    path('shops/', views.shop_list, name='shop_list'),
    path('shop/<int:shop_id>/', views.shop_detail, name='shop_detail'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('payfast-return/', views.payfast_return, name='payfast_return'),
    path('payfast-notify/', views.payfast_notify, name='payfast_notify'),
    path('order_confirmation/', views.order_confirmation, name='order_confirmation'),
    path('store-profile/', views.store_profile, name='store_profile'),
    path('store-profile-free/', views.store_profile_free, name='store_profile_free'),
    path('manage-products/<int:store_id>/', views.manage_products, name='manage_products'),
    path('store/<int:store_id>/add-product/', views.add_product_to_store, name='add_product_to_store'),
    path('product/<int:product_id>/edit/', views.edit_product, name='edit_product'),
    path('product/<int:product_id>/delete/', views.delete_product, name='delete_product'),
    path('thank_you/', views.thank_you, name='thank_you'),

]
