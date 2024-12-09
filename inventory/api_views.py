# inventory/api_views.py
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
from .models import InventoryItem, Warehouse, SubWarehouse
from .serializers import InventoryItemSerializer, WarehouseSerializer, SubWarehouseSerializer

class WarehouseViewSet(viewsets.ModelViewSet):
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer

    def create(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                return super().create(request, *args, **kwargs)
        except Exception as e:
            return Response(
                {'message': f'Error creating warehouse: {str(e)}'},
                status=status.HTTP_400_BAD_REQUEST
            )

class SubWarehouseViewSet(viewsets.ModelViewSet):
    queryset = SubWarehouse.objects.all()
    serializer_class = SubWarehouseSerializer

    def create(self, request, *args, **kwargs):
        try:
            warehouse_id = request.data.get('warehouse')
            if not warehouse_id:
                raise ValidationError('Warehouse is required')
            
            try:
                warehouse = Warehouse.objects.get(id=warehouse_id)
            except ObjectDoesNotExist:
                raise ValidationError('Invalid warehouse')

            with transaction.atomic():
                return super().create(request, *args, **kwargs)
        except ValidationError as e:
            return Response(
                {'message': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {'message': f'Error creating sub-warehouse: {str(e)}'},
                status=status.HTTP_400_BAD_REQUEST
            )

class InventoryItemViewSet(viewsets.ModelViewSet):
    queryset = InventoryItem.objects.all()
    serializer_class = InventoryItemSerializer

    def create(self, request, *args, **kwargs):
        try:
            # Validate warehouse and subwarehouse relationship
            warehouse_id = request.data.get('warehouse')
            subwarehouse_id = request.data.get('subwarehouse')
            
            if subwarehouse_id and not warehouse_id:
                raise ValidationError('Cannot assign to subwarehouse without a warehouse')
            
            if subwarehouse_id:
                try:
                    subwarehouse = SubWarehouse.objects.get(id=subwarehouse_id)
                    if str(subwarehouse.warehouse.id) != str(warehouse_id):
                        raise ValidationError('Subwarehouse does not belong to the selected warehouse')
                except ObjectDoesNotExist:
                    raise ValidationError('Invalid subwarehouse')

            with transaction.atomic():
                return super().create(request, *args, **kwargs)
        except ValidationError as e:
            return Response(
                {'message': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {'message': f'Error creating inventory item: {str(e)}'},
                status=status.HTTP_400_BAD_REQUEST
            )

    def update(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                return super().update(request, *args, **kwargs)
        except Exception as e:
            return Response(
                {'message': f'Error updating inventory item: {str(e)}'},
                status=status.HTTP_400_BAD_REQUEST
            )

    def destroy(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                return super().destroy(request, *args, **kwargs)
        except Exception as e:
            return Response(
                {'message': f'Error deleting inventory item: {str(e)}'},
                status=status.HTTP_400_BAD_REQUEST
            )
