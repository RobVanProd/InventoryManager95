from rest_framework import serializers
from ..models import InventoryItem
from .warehouse import WarehouseSerializer, SubWarehouseSerializer


class InventoryItemSerializer(serializers.ModelSerializer):
    warehouse_details = WarehouseSerializer(source='warehouse', read_only=True)
    sub_warehouse_details = SubWarehouseSerializer(source='sub_warehouse', read_only=True)

    class Meta:
        model = InventoryItem
        fields = [
            'id', 'name', 'description', 'quantity',
            'warehouse', 'sub_warehouse',
            'warehouse_details', 'sub_warehouse_details',
            'created_at', 'updated_at', 'unit_price', 'is_active'
        ]
