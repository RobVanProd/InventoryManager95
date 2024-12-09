from django.core.management.base import BaseCommand
from inventory.models import InventoryItem
from inventory.services.reorder_service import ReorderService


class Command(BaseCommand):
    help = 'Check stock levels for all items and create alerts/reorders as needed'

    def handle(self, *args, **options):
        self.stdout.write('Starting stock level check...')
        
        # Get all active items
        items = InventoryItem.objects.filter(is_active=True)
        alerts_created = 0
        orders_created = 0
        
        for item in items:
            # Check if item has reorder point and it's active
            if hasattr(item, 'reorder_point') and item.reorder_point.is_active:
                # Process reorder if needed
                purchase_order = ReorderService.process_reorder(item)
                if purchase_order:
                    orders_created += 1
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'Created purchase order for {item.name}'
                        )
                    )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Stock level check completed. Created {orders_created} purchase orders.'
            )
        )
