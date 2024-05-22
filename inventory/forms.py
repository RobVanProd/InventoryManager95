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

class TransferItemForm(forms.Form):
    item = forms.ModelChoiceField(queryset=InventoryItem.objects.all())
    source = forms.ChoiceField(choices=[('warehouse', 'Warehouse'), ('subwarehouse', 'SubWarehouse')])
    destination = forms.ChoiceField(choices=[('warehouse', 'Warehouse'), ('subwarehouse', 'SubWarehouse')])
    quantity = forms.IntegerField(min_value=1)
