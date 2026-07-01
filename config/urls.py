from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LogoutView
from stationery.views import custom_login

urlpatterns = [
    path('admin/', admin.site.urls),

    # Custom login page with User/Admin dropdown
    path('accounts/login/', custom_login, name='login'),

    # Logout
    path(
        'accounts/logout/',
        LogoutView.as_view(),
        name='logout'
    ),

    # Stationery application URLs
    path('', include('stationery.urls')),
]