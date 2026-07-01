from django.urls import path
from . import views

urlpatterns = [
    path('', views.create_requisition, name='create_requisition'),

    path(
        'status/',
        views.view_requests,
        name='view_requests'
    ),

    path(
        'dashboard/',
        views.dashboard,
        name='dashboard'
    ),

    path(
        'export/',
        views.export_excel,
        name='export_excel'
    ),
]