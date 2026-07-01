from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),

    path('accounts/login/', custom_login, name='login'),

    path(
        'accounts/logout/',
        LogoutView.as_view(),
        name='logout'
    ),

    path('', include('stationery.urls')),
]