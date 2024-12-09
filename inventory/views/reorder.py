from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from ..models import ReorderPoint, StockAlert, InventoryItem
from ..serializers import ReorderPointSerializer, StockAlertSerializer
from ..services.reorder_service import ReorderService


class ReorderPointViewSet(viewsets.ModelViewSet):
    queryset = ReorderPoint.objects.all()
    serializer_class = ReorderPointSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['post'])
    def check_reorder(self, request, pk=None):
        """
        Manually check if reorder is needed for an item.
        """
        reorder_point = self.get_object()
        if reorder_point.calculate_reorder_needed():
            purchase_order = ReorderService.process_reorder(reorder_point.item)
            if purchase_order:
                return Response({
                    'message': 'Purchase order created successfully',
                    'purchase_order_id': purchase_order.id
                })
            return Response({
                'message': 'Reorder needed but could not create purchase order'
            }, status=status.HTTP_400_BAD_REQUEST)
        return Response({
            'message': 'No reorder needed'
        })


class StockAlertViewSet(viewsets.ModelViewSet):
    queryset = StockAlert.objects.all()
    serializer_class = StockAlertSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = StockAlert.objects.all()
        # Filter by active status
        is_active = self.request.query_params.get('is_active', None)
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() == 'true')
        # Filter by alert type
        alert_type = self.request.query_params.get('alert_type', None)
        if alert_type:
            queryset = queryset.filter(alert_type=alert_type.upper())
        # Filter by priority
        priority = self.request.query_params.get('priority', None)
        if priority:
            queryset = queryset.filter(priority=priority.upper())
        return queryset

    @action(detail=True, methods=['post'])
    def resolve(self, request, pk=None):
        """
        Mark an alert as resolved.
        """
        alert = self.get_object()
        alert.resolve()
        return Response({
            'message': 'Alert resolved successfully'
        })

    @action(detail=False, methods=['post'])
    def check_item(self, request):
        """
        Manually check stock levels for a specific item.
        """
        item_id = request.data.get('item_id')
        if not item_id:
            return Response({
                'error': 'item_id is required'
            }, status=status.HTTP_400_BAD_REQUEST)

        item = get_object_or_404(InventoryItem, id=item_id)
        alert = ReorderService.check_stock_levels(item)
        
        if alert:
            return Response({
                'message': 'Alert created',
                'alert': StockAlertSerializer(alert).data
            })
        return Response({
            'message': 'No alert needed'
        })
