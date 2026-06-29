from django.contrib import admin
from django.urls import path, include
from stationery.views import CustomLoginView

urlpatterns = [
    path('admin/', admin.site.urls),

    path('accounts/login/', CustomLoginView.as_view(), name='login'),

    path('accounts/', include('django.contrib.auth.urls')),

    path('', include('stationery.urls')),
]
from .views import custom_login

urlpatterns = [
    path('accounts/login/', custom_login, name='login'),
]