from django.db import models
from django.core.validators import MinValueValidator
from .inventory_item import InventoryItem
from .supplier import Supplier


class ReorderPoint(models.Model):
    """
    Defines when an item should be reordered based on stock levels and other factors.
    """
    item = models.OneToOneField(InventoryItem, on_delete=models.CASCADE, related_name='reorder_point')
    minimum_quantity = models.IntegerField(
        validators=[MinValueValidator(0)],
        help_text="Minimum quantity before reorder is triggered"
    )
    reorder_quantity = models.IntegerField(
        validators=[MinValueValidator(1)],
        help_text="Quantity to order when reorder point is reached"
    )
    preferred_supplier = models.ForeignKey(
        Supplier,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="Preferred supplier for reordering this item"
    )
    safety_stock = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        help_text="Extra stock kept to prevent stockouts"
    )
    lead_time_days = models.IntegerField(
        default=1,
        validators=[MinValueValidator(1)],
        help_text="Expected number of days between order and delivery"
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Whether automatic reordering is enabled for this item"
    )
    last_reorder_date = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Date of the last automatic reorder"
    )
    seasonal_adjustment = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=1.00,
        help_text="Seasonal adjustment factor for reorder calculations"
    )

    def __str__(self):
        return f"Reorder Point for {self.item.name}"

    def calculate_reorder_needed(self) -> bool:
        """
        Determines if a reorder is needed based on current stock levels and safety stock.
        """
        current_stock = self.item.quantity
        return current_stock <= (self.minimum_quantity + self.safety_stock)

    def calculate_optimal_order_quantity(self) -> int:
        """
        Calculates the optimal order quantity considering seasonal adjustments.
        """
        base_quantity = self.reorder_quantity
        return int(base_quantity * float(self.seasonal_adjustment))


class StockAlert(models.Model):
    """
    Records alerts for low stock and other inventory-related notifications.
    """
    ALERT_TYPES = [
        ('LOW_STOCK', 'Low Stock'),
        ('STOCKOUT', 'Stockout'),
        ('REORDER_FAILED', 'Reorder Failed'),
        ('ORDER_PLACED', 'Order Placed'),
        ('DELIVERY_DUE', 'Delivery Due'),
    ]

    ALERT_PRIORITIES = [
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
        ('CRITICAL', 'Critical'),
    ]

    item = models.ForeignKey(
        InventoryItem,
        on_delete=models.CASCADE,
        related_name='stock_alerts'
    )
    alert_type = models.CharField(
        max_length=20,
        choices=ALERT_TYPES
    )
    priority = models.CharField(
        max_length=10,
        choices=ALERT_PRIORITIES,
        default='MEDIUM'
    )
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="When the alert was resolved"
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Whether the alert is still active"
    )
    auto_reorder_triggered = models.BooleanField(
        default=False,
        help_text="Whether this alert triggered an automatic reorder"
    )
    related_purchase_order = models.ForeignKey(
        'PurchaseOrder',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="Purchase order created in response to this alert"
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.get_alert_type_display()} - {self.item.name}"

    def resolve(self):
        """
        Marks the alert as resolved.
        """
        from django.utils import timezone
        self.resolved_at = timezone.now()
        self.is_active = False
        self.save()
