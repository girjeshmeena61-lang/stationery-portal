from django.urls import path
from .views import (
    create_requisition,
    view_requests,
    dashboard,
    export_excel,
)

urlpatterns = [
    path('', create_requisition, name='create_requisition'),
    path('status/', view_requests, name='view_requests'),
    path('dashboard/', dashboard, name='dashboard'),
    path('export/', export_excel, name='export_excel'),
]