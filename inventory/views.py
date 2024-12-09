from django.shortcuts import render, redirect
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import InventoryItem, Warehouse, SubWarehouse
from .serializers import InventoryItemSerializer, WarehouseSerializer, SubWarehouseSerializer
from django.db.models import Sum, Count, F, Q, DecimalField
from django.db.models.functions import Coalesce
from django.utils import timezone

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_items(request):
    items = InventoryItem.objects.all()
    serializer = InventoryItemSerializer(items, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_item(request):
    serializer = InventoryItemSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'Item added successfully', 'data': serializer.data}, status=201)
    return Response(serializer.errors, status=400)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_item(request, item_id):
    try:
        item = InventoryItem.objects.get(id=item_id)
        item.delete()
        return Response({'message': 'Item deleted successfully'}, status=200)
    except InventoryItem.DoesNotExist:
        return Response({'message': 'Item not found'}, status=404)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_dashboard_stats(request):
    # Get total counts
    total_items = InventoryItem.objects.count()
    total_warehouses = Warehouse.objects.count()
    total_subwarehouses = SubWarehouse.objects.count()

    # Get total inventory value
    total_value = InventoryItem.objects.filter(price__isnull=False).aggregate(
        total=Coalesce(
            Sum(
                F('price') * F('quantity'),
                output_field=DecimalField(max_digits=10, decimal_places=2)
            ),
            0,
            output_field=DecimalField(max_digits=10, decimal_places=2)
        )
    )['total']

    # Get low stock items (less than 10 units)
    low_stock_items = InventoryItem.objects.filter(quantity__lt=10).count()

    # Get items by warehouse
    items_by_warehouse = (
        InventoryItem.objects.values('warehouse__name')
        .annotate(count=Count('id'))
        .order_by('-count')
    )

    # Get recent items (last 7 days)
    recent_items = InventoryItem.objects.filter(
        created_at__gte=timezone.now() - timezone.timedelta(days=7)
    ).count()

    return Response({
        'total_items': total_items,
        'total_warehouses': total_warehouses,
        'total_subwarehouses': total_subwarehouses,
        'total_value': float(total_value),
        'low_stock_items': low_stock_items,
        'items_by_warehouse': list(items_by_warehouse),
        'recent_items': recent_items,
    })

class WarehouseViewSet(viewsets.ModelViewSet):
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer
    permission_classes = [permissions.IsAuthenticated]

class SubWarehouseViewSet(viewsets.ModelViewSet):
    queryset = SubWarehouse.objects.all()
    serializer_class = SubWarehouseSerializer
    permission_classes = [permissions.IsAuthenticated]

class InventoryItemViewSet(viewsets.ModelViewSet):
    queryset = InventoryItem.objects.all()
    serializer_class = InventoryItemSerializer
    permission_classes = [permissions.IsAuthenticated]
