from django.contrib import admin
from .models import Inventory, Requisition


@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ('item_name', 'available_qty', 'minimum_qty', 'unit')


@admin.register(Requisition)
class RequisitionAdmin(admin.ModelAdmin):
    list_display = (
        'item',
        'department',
        'requested_by',
        'requested_qty',
        'approved_qty',
        'status',
        'created_at'
    )
