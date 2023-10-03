from django.contrib.auth import views as auth_views

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Define a home view
    path('home2/', views.home2, name='home_shops'),
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
    path('store-profile/', views.store_profile, name='store_profile'),
    path('manage-products/<int:store_id>/', views.manage_products, name='manage_products'),
    path('store/<int:store_id>/add-product/', views.add_product_to_store, name='add_product_to_store'),

    # Edit an existing product
    path('product/<int:product_id>/edit/', views.edit_product, name='edit_product'),

    # Delete an existing product
    path('product/<int:product_id>/delete/', views.delete_product, name='delete_product'),

    # Add more URL patterns for other views as needed
]
