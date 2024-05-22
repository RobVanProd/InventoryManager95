from django.shortcuts import render, redirect
from .models import InventoryItem, Warehouse, SubWarehouse
from .forms import InventoryItemForm, TransferItemForm
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
            item = form.save(commit=False)
            if request.POST.get('warehouse'):
                item.warehouse = Warehouse.objects.get(id=request.POST['warehouse'])
            else:
                item.warehouse = None

            if request.POST.get('subwarehouse'):
                item.subwarehouse = SubWarehouse.objects.get(id=request.POST['subwarehouse'])
            else:
                item.subwarehouse = None

            item.save()
            return redirect('view_items')
    else:
        form = InventoryItemForm()
    return render(request, 'inventory/add_item.html', {'form': form})

@login_required
def view_items(request):
    user_subwarehouse = request.user.subwarehouse
    items = InventoryItem.objects.filter(subwarehouse=user_subwarehouse)
    return render(request, 'inventory/view_items.html', {'items': items})

@login_required
def transfer_item(request):
    if request.method == 'POST':
        form = TransferItemForm(request.POST)
        if form.is_valid():
            item = form.cleaned_data['item']
            source = form.cleaned_data['source']
            destination = form.cleaned_data['destination']
            quantity = form.cleaned_data['quantity']

            if source == 'warehouse' and item.warehouse:
                item.warehouse.quantity -= quantity
            elif source == 'subwarehouse' and item.subwarehouse:
                item.subwarehouse.quantity -= quantity

            if destination == 'warehouse':
                item.warehouse = Warehouse.objects.get(id=request.POST['destination_id'])
                item.warehouse.quantity += quantity
            elif destination == 'subwarehouse':
                item.subwarehouse = SubWarehouse.objects.get(id=request.POST['destination_id'])
                item.subwarehouse.quantity += quantity

            item.save()
            return redirect('view_items')
    else:
        form = TransferItemForm()
    return render(request, 'inventory/transfer_item.html', {'form': form})

@login_required
def delete_item(request, item_id):
    item = InventoryItem.objects.get(id=item_id)
    if request.method == 'POST':
        item.delete()
        return redirect('view_items')
    return render(request, 'inventory/delete_item.html', {'item': item})
