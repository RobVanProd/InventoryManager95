# inventory/forms.py
from django import forms
from .models import InventoryItem, Warehouse, SubWarehouse

class WarehouseForm(forms.ModelForm):
    class Meta:
        model = Warehouse
        fields = ['name', 'location']

class SubWarehouseForm(forms.ModelForm):
    class Meta:
        model = SubWarehouse
        fields = ['name', 'warehouse', 'user']

class InventoryItemForm(forms.ModelForm):
    class Meta:
        model = InventoryItem
        fields = ['name', 'quantity', 'description', 'price', 'warehouse', 'subwarehouse']
