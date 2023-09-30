from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('shopciti_app.urls')),  # Include your app's URL patterns
    path('admin/', admin.site.urls),
]
