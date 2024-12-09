from rest_framework import serializers
from ..models.reorder import ReorderPoint, StockAlert


class ReorderPointSerializer(serializers.ModelSerializer):
    item_name = serializers.CharField(source='item.name', read_only=True)
    preferred_supplier_name = serializers.CharField(source='preferred_supplier.name', read_only=True)
    current_stock = serializers.IntegerField(source='item.quantity', read_only=True)
    reorder_needed = serializers.BooleanField(source='calculate_reorder_needed', read_only=True)
    optimal_order_quantity = serializers.IntegerField(source='calculate_optimal_order_quantity', read_only=True)

    class Meta:
        model = ReorderPoint
        fields = [
            'id', 'item', 'item_name', 'minimum_quantity', 'reorder_quantity',
            'preferred_supplier', 'preferred_supplier_name', 'safety_stock',
            'lead_time_days', 'is_active', 'last_reorder_date',
            'seasonal_adjustment', 'current_stock', 'reorder_needed',
            'optimal_order_quantity'
        ]
        read_only_fields = ['last_reorder_date']


class StockAlertSerializer(serializers.ModelSerializer):
    item_name = serializers.CharField(source='item.name', read_only=True)
    alert_type_display = serializers.CharField(source='get_alert_type_display', read_only=True)
    priority_display = serializers.CharField(source='get_priority_display', read_only=True)

    class Meta:
        model = StockAlert
        fields = [
            'id', 'item', 'item_name', 'alert_type', 'alert_type_display',
            'priority', 'priority_display', 'message', 'created_at',
            'resolved_at', 'is_active', 'auto_reorder_triggered',
            'related_purchase_order'
        ]
        read_only_fields = ['created_at', 'resolved_at']

    def create(self, validated_data):
        """
        Create a new stock alert and check if auto-reorder should be triggered.
        """
        alert = super().create(validated_data)
        
        # Check if this is a low stock alert and auto-reorder is enabled
        if (alert.alert_type == 'LOW_STOCK' and 
            hasattr(alert.item, 'reorder_point') and 
            alert.item.reorder_point.is_active):
            
            reorder_point = alert.item.reorder_point
            if reorder_point.calculate_reorder_needed():
                # Mark that auto-reorder was triggered
                alert.auto_reorder_triggered = True
                alert.save()
                
                # The actual reorder logic will be handled by the view
                # to avoid circular imports and keep the serializer focused
                # on data transformation
        
        return alert
