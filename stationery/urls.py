from django.urls import path
from . import views

urlpatterns = [
    path('', views.requisition_form, name='requisition_form'),
    path('status/', views.request_status, name='request_status'),
    path('dashboard/', views.dashboard, name='dashboard'),
]