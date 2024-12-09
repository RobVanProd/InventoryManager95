from django.db import transaction
from django.utils import timezone
from typing import Optional, Tuple

from ..models import (
    InventoryItem,
    ReorderPoint,
    StockAlert,
    PurchaseOrder,
    PurchaseOrderItem,
    Supplier
)


class ReorderService:
    @staticmethod
    def check_stock_levels(item: InventoryItem) -> Optional[StockAlert]:
        """
        Check stock levels for an item and create alerts if necessary.
        Returns the created alert if stock is low, None otherwise.
        """
        if not hasattr(item, 'reorder_point'):
            return None

        reorder_point = item.reorder_point
        current_stock = item.quantity

        if current_stock <= 0:
            # Create stockout alert
            return StockAlert.objects.create(
                item=item,
                alert_type='STOCKOUT',
                priority='CRITICAL',
                message=f'Item {item.name} is out of stock!'
            )
        elif current_stock <= reorder_point.minimum_quantity:
            # Create low stock alert
            return StockAlert.objects.create(
                item=item,
                alert_type='LOW_STOCK',
                priority='HIGH',
                message=f'Item {item.name} has reached its reorder point. Current stock: {current_stock}'
            )
        return None

    @staticmethod
    def get_preferred_supplier(item: InventoryItem) -> Optional[Supplier]:
        """
        Get the preferred supplier for an item, falling back to the most reliable supplier.
        """
        if hasattr(item, 'reorder_point') and item.reorder_point.preferred_supplier:
            return item.reorder_point.preferred_supplier

        # Fall back to the supplier with the highest reliability rating
        return Supplier.objects.filter(
            is_active=True
        ).order_by('-reliability_rating').first()

    @classmethod
    @transaction.atomic
    def create_purchase_order(cls, item: InventoryItem, alert: StockAlert) -> Tuple[PurchaseOrder, bool]:
        """
        Create a purchase order for an item that needs reordering.
        Returns a tuple of (purchase_order, created).
        """
        if not hasattr(item, 'reorder_point'):
            return None, False

        reorder_point = item.reorder_point
        supplier = cls.get_preferred_supplier(item)

        if not supplier:
            # Create alert for no supplier available
            StockAlert.objects.create(
                item=item,
                alert_type='REORDER_FAILED',
                priority='HIGH',
                message=f'Could not reorder {item.name}: No suitable supplier found'
            )
            return None, False

        # Calculate order quantity
        order_quantity = reorder_point.calculate_optimal_order_quantity()

        # Create purchase order
        purchase_order = PurchaseOrder.objects.create(
            supplier=supplier,
            status='DRAFT',
            expected_delivery_date=timezone.now() + timezone.timedelta(days=reorder_point.lead_time_days)
        )

        # Add item to purchase order
        PurchaseOrderItem.objects.create(
            purchase_order=purchase_order,
            item=item,
            quantity=order_quantity,
            unit_price=item.unit_price
        )

        # Update alert with purchase order reference
        alert.related_purchase_order = purchase_order
        alert.auto_reorder_triggered = True
        alert.save()

        # Update reorder point last order date
        reorder_point.last_reorder_date = timezone.now()
        reorder_point.save()

        return purchase_order, True

    @classmethod
    def process_reorder(cls, item: InventoryItem) -> Optional[PurchaseOrder]:
        """
        Process the complete reorder workflow for an item.
        Returns the created purchase order if successful, None otherwise.
        """
        # Check stock levels and create alert if necessary
        alert = cls.check_stock_levels(item)
        if not alert or alert.alert_type not in ['LOW_STOCK', 'STOCKOUT']:
            return None

        # Create purchase order
        purchase_order, created = cls.create_purchase_order(item, alert)
        if not created:
            return None

        return purchase_order
