from django.contrib.auth import views as auth_views

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home1, name='home_shops'),  # Define a home view
    path('home2/', views.home2, name='home2'),
    path('products/', views.product_list, name='product_list'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='shopciti_app/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('user-profile/', views.user_profile, name='user_profile'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('register-store/', views.register_store, name='register_store'),
    path('registration-success/', views.registration_success, name='registration_success'),
    path('registration-failure/', views.registration_failure, name='registration_failure'),
    path('shops/', views.shop_list, name='shop_list'),
    path('shop/<int:shop_id>/', views.shop_detail, name='shop_detail'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('cart/', views.cart, name='cart'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('update_cart/<int:product_id>/', views.update_cart, name='update_cart'),
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
