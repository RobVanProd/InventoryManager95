# . inventory/serializers.py
from rest_framework import serializers
from .models import InventoryItem, Warehouse, SubWarehouse

class WarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields = '__all__'

class SubWarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubWarehouse
        fields = '__all__'

class InventoryItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryItem
        fields = '__all__'
