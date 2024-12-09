from celery import shared_task
from django.core.management import call_command
from .models import InventoryItem
from .services.reorder_service import ReorderService


@shared_task
def check_stock_levels():
    """
    Celery task to check stock levels and create alerts/reorders as needed.
    """
    # Get all active items
    items = InventoryItem.objects.filter(is_active=True)
    orders_created = 0
    
    for item in items:
        # Check if item has reorder point and it's active
        if hasattr(item, 'reorder_point') and item.reorder_point.is_active:
            # Process reorder if needed
            purchase_order = ReorderService.process_reorder(item)
            if purchase_order:
                orders_created += 1
    
    return f'Stock level check completed. Created {orders_created} purchase orders.'
