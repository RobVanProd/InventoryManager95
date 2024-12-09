# Register your models here.
# inventory/admin.py
from django.contrib import admin
from .models import (
    Warehouse, SubWarehouse, InventoryItem,
    Supplier, SupplierContact,
    PurchaseOrder, PurchaseOrderItem
)

# Register existing models
admin.site.register(Warehouse)
admin.site.register(SubWarehouse)
admin.site.register(InventoryItem)

# Register new supplier-related models
@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'contact_name', 'email', 'reliability_rating', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name', 'code', 'contact_name', 'email']
    readonly_fields = ['reliability_rating', 'average_lead_time', 'on_time_delivery_rate']

@admin.register(SupplierContact)
class SupplierContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'supplier', 'role', 'email', 'is_primary']
    list_filter = ['is_primary', 'supplier']
    search_fields = ['name', 'email', 'supplier__name']

@admin.register(PurchaseOrder)
class PurchaseOrderAdmin(admin.ModelAdmin):
    list_display = ['po_number', 'supplier', 'order_date', 'status', 'total']
    list_filter = ['status', 'supplier']
    search_fields = ['po_number', 'supplier__name']
    readonly_fields = ['po_number', 'total', 'created_by', 'created_at', 'updated_at']

@admin.register(PurchaseOrderItem)
class PurchaseOrderItemAdmin(admin.ModelAdmin):
    list_display = ['purchase_order', 'item', 'quantity', 'unit_price', 'subtotal']
    list_filter = ['purchase_order__supplier']
    search_fields = ['purchase_order__po_number', 'item__name']
    readonly_fields = ['subtotal']
