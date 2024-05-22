from django.shortcuts import render, get_object_or_404, redirect
from .models import InventoryItem
from .forms import InventoryItemForm

def home(request):
    return render(request, 'inventory/home.html')

def add_item(request):
    if request.method == 'POST':
        form = InventoryItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('view_items')
    else:
        form = InventoryItemForm()
    return render(request, 'inventory/add_item.html', {'form': form})

def view_items(request):
    items = InventoryItem.objects.all()
    return render(request, 'inventory/view_items.html', {'items': items})
