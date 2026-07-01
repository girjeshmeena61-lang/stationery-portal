from django.urls import path
from . import views

urlpatterns = [
    path('', views.create_requisition, name='create_requisition'),
    path('status/', views.request_status, name='request_status'),
    path('dashboard/', views.dashboard, name='dashboard'),
]