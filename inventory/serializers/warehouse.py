from rest_framework import serializers
from ..models import Warehouse, SubWarehouse


class SubWarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubWarehouse
        fields = ['id', 'warehouse', 'name', 'location', 'capacity', 'is_active']


class WarehouseSerializer(serializers.ModelSerializer):
    sub_warehouses = SubWarehouseSerializer(many=True, read_only=True, source='subwarehouse_set')

    class Meta:
        model = Warehouse
        fields = ['id', 'name', 'location', 'capacity', 'is_active', 'sub_warehouses']
