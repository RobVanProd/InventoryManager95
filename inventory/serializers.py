# . inventory/serializers.py
from rest_framework import serializers
from .models import InventoryItem, Warehouse, SubWarehouse

class WarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields = ['id', 'name', 'location']

    def validate_name(self, value):
        if len(value.strip()) < 2:
            raise serializers.ValidationError("Warehouse name must be at least 2 characters long")
        return value.strip()

class SubWarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubWarehouse
        fields = ['id', 'name', 'warehouse', 'user']

    def validate_name(self, value):
        if len(value.strip()) < 2:
            raise serializers.ValidationError("Sub-warehouse name must be at least 2 characters long")
        return value.strip()

    def validate(self, data):
        if 'warehouse' not in data:
            raise serializers.ValidationError("Warehouse is required")
        return data

class InventoryItemSerializer(serializers.ModelSerializer):
    warehouse_name = serializers.CharField(source='warehouse.name', read_only=True)
    subwarehouse_name = serializers.CharField(source='subwarehouse.name', read_only=True)

    class Meta:
        model = InventoryItem
        fields = [
            'id', 'name', 'quantity', 'description', 'price',
            'warehouse', 'warehouse_name',
            'subwarehouse', 'subwarehouse_name'
        ]

    def validate_name(self, value):
        if len(value.strip()) < 2:
            raise serializers.ValidationError("Item name must be at least 2 characters long")
        return value.strip()

    def validate_quantity(self, value):
        if value < 0:
            raise serializers.ValidationError("Quantity cannot be negative")
        return value

    def validate_price(self, value):
        if value is not None and value < 0:
            raise serializers.ValidationError("Price cannot be negative")
        return value

    def validate(self, data):
        if 'subwarehouse' in data and data['subwarehouse'] is not None:
            if 'warehouse' not in data or data['warehouse'] is None:
                raise serializers.ValidationError({
                    "warehouse": "Warehouse is required when specifying a sub-warehouse"
                })
            
            if data['subwarehouse'].warehouse.id != data['warehouse'].id:
                raise serializers.ValidationError({
                    "subwarehouse": "Selected sub-warehouse does not belong to the selected warehouse"
                })
        
        return data
