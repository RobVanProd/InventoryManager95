from rest_framework import serializers
from ..models.purchase_order import PurchaseOrder, PurchaseOrderItem
from ..models.supplier import Supplier


class PurchaseOrderItemSerializer(serializers.ModelSerializer):
    item_name = serializers.CharField(source='item.name', read_only=True)
    
    class Meta:
        model = PurchaseOrderItem
        fields = [
            'id', 'item', 'item_name', 'quantity', 'unit_price',
            'subtotal', 'received_quantity', 'received_date'
        ]
        read_only_fields = ['id', 'subtotal']

    def validate(self, data):
        """Validate that received quantity doesn't exceed ordered quantity"""
        if 'received_quantity' in data:
            if data['received_quantity'] > data.get('quantity', self.instance.quantity):
                raise serializers.ValidationError({
                    "received_quantity": "Cannot receive more items than ordered"
                })
        return data


class PurchaseOrderSerializer(serializers.ModelSerializer):
    items = PurchaseOrderItemSerializer(many=True)
    supplier_name = serializers.CharField(source='supplier.name', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = PurchaseOrder
        fields = [
            'id', 'po_number', 'supplier', 'supplier_name',
            'order_date', 'expected_delivery_date',
            'actual_delivery_date', 'status', 'status_display',
            'shipping_address', 'shipping_method',
            'tracking_number', 'subtotal', 'tax',
            'shipping_cost', 'total', 'currency',
            'notes', 'created_at', 'updated_at',
            'created_by', 'items'
        ]
        read_only_fields = [
            'id', 'po_number', 'subtotal', 'total',
            'created_at', 'updated_at', 'created_by'
        ]

    def validate_expected_delivery_date(self, value):
        """Ensure expected delivery date is in the future"""
        if value <= self.context['request'].data.get('order_date'):
            raise serializers.ValidationError(
                "Expected delivery date must be after order date"
            )
        return value

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        validated_data['created_by'] = self.context['request'].user
        purchase_order = PurchaseOrder.objects.create(**validated_data)
        
        for item_data in items_data:
            PurchaseOrderItem.objects.create(
                purchase_order=purchase_order,
                **item_data
            )
        
        return purchase_order

    def update(self, instance, validated_data):
        items_data = validated_data.pop('items', None)
        
        # Update PO fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        if items_data is not None:
            # Update items
            instance.items.all().delete()
            for item_data in items_data:
                PurchaseOrderItem.objects.create(
                    purchase_order=instance,
                    **item_data
                )
        
        return instance
