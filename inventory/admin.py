# Register your models here.
# inventory/admin.py
from django.contrib import admin
from .models import Warehouse, SubWarehouse, InventoryItem

admin.site.register(Warehouse)
admin.site.register(SubWarehouse)
admin.site.register(InventoryItem)
