from django.contrib.auth import views as auth_views

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Define a home view

    path('products/', views.product_list, name='product_list'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='shopciti_app/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register-store/', views.register_store, name='register_store'),
    path('registration-success/', views.registration_success, name='registration_success'),
    path('registration-failure/', views.registration_failure, name='registration_failure'),
    path('shops/', views.shop_list, name='shops'),
    path('store-profile/', views.store_profile, name='store_profile'),


    # Add more URL patterns for other views as needed
]
