# inventory/views.py
from django.shortcuts import render, redirect
from .models import InventoryItem, Warehouse, SubWarehouse
from .forms import InventoryItemForm, WarehouseForm, SubWarehouseForm
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, 'inventory/home.html')

@login_required
def add_warehouse(request):
    if request.method == 'POST':
        form = WarehouseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('warehouse_list')
    else:
        form = WarehouseForm()
    return render(request, 'inventory/add_warehouse.html', {'form': form})

@login_required
def add_subwarehouse(request):
    if request.method == 'POST':
        form = SubWarehouseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('subwarehouse_list')
    else:
        form = SubWarehouseForm()
    return render(request, 'inventory/add_subwarehouse.html', {'form': form})

@login_required
def add_item(request):
    if request.method == 'POST':
        form = InventoryItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('item_list')
    else:
        form = InventoryItemForm()
    return render(request, 'inventory/add_item.html', {'form': form})

@login_required
def view_items(request):
    user_subwarehouse = request.user.subwarehouse
    items = InventoryItem.objects.filter(subwarehouse=user_subwarehouse)
    return render(request, 'inventory/view_items.html', {'items': items})
