# inventory/api_views.py
from rest_framework import viewsets
from .models import InventoryItem, Warehouse, SubWarehouse
from .serializers import InventoryItemSerializer, WarehouseSerializer, SubWarehouseSerializer

class WarehouseViewSet(viewsets.ModelViewSet):
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer

class SubWarehouseViewSet(viewsets.ModelViewSet):
    queryset = SubWarehouse.objects.all()
    serializer_class = SubWarehouseSerializer

class InventoryItemViewSet(viewsets.ModelViewSet):
    queryset = InventoryItem.objects.all()
    serializer_class = InventoryItemSerializer
