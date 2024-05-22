# inventory/views.py
from django.shortcuts import render, redirect
from .forms import InventoryItemForm

def add_item(request):
    if request.method == 'POST':
        form = InventoryItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')  # Adjust the redirect as necessary
    else:
        form = InventoryItemForm()
    return render(request, 'inventory/add_item.html', {'form': form})

def edit_item(request, pk):
    item = get_object_or_404(InventoryItem, pk=pk)
    if request.method == 'POST':
        form = InventoryItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('home')  # Adjust the redirect as necessary
    else:
        form = InventoryItemForm(instance=item)
    return render(request, 'inventory/edit_item.html', {'form': form})
