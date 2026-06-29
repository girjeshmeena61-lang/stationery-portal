from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # Keep Django logout functionality
    path('accounts/logout/', include('django.contrib.auth.urls')),

    # Your app URLs
    path('', include('stationery.urls')),
]