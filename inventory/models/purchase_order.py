from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone
from decimal import Decimal


class PurchaseOrder(models.Model):
    """
    Model representing a purchase order to a supplier.
    """
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('confirmed', 'Confirmed'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]

    supplier = models.ForeignKey(
        'Supplier',
        on_delete=models.PROTECT,
        related_name='purchase_orders'
    )
    po_number = models.CharField(max_length=50, unique=True)
    order_date = models.DateTimeField(default=timezone.now)
    expected_delivery_date = models.DateTimeField()
    actual_delivery_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='draft'
    )
    
    # Shipping details
    shipping_address = models.TextField()
    shipping_method = models.CharField(max_length=100)
    tracking_number = models.CharField(max_length=100, blank=True)
    
    # Financial details
    subtotal = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    tax = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
        default=Decimal('0.00')
    )
    shipping_cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
        default=Decimal('0.00')
    )
    total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    currency = models.CharField(max_length=3, default='USD')
    
    # Metadata
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        'auth.User',
        on_delete=models.PROTECT,
        related_name='created_purchase_orders'
    )

    class Meta:
        ordering = ['-order_date']

    def __str__(self):
        return f"PO-{self.po_number} ({self.supplier.name})"

    def save(self, *args, **kwargs):
        # Calculate total
        self.total = self.subtotal + self.tax + self.shipping_cost
        
        # Generate PO number if not set
        if not self.po_number:
            last_po = PurchaseOrder.objects.order_by('-id').first()
            if last_po:
                last_number = int(last_po.po_number.split('-')[1])
                self.po_number = f"PO-{str(last_number + 1).zfill(6)}"
            else:
                self.po_number = "PO-000001"
        
        super().save(*args, **kwargs)
        
        # Update supplier metrics if delivered
        if self.status == 'delivered' and self.actual_delivery_date:
            self.supplier.update_performance_metrics()


class PurchaseOrderItem(models.Model):
    """
    Individual items within a purchase order.
    """
    purchase_order = models.ForeignKey(
        PurchaseOrder,
        on_delete=models.CASCADE,
        related_name='items'
    )
    item = models.ForeignKey(
        'InventoryItem',
        on_delete=models.PROTECT,
        related_name='purchase_order_items'
    )
    quantity = models.IntegerField(validators=[MinValueValidator(1)])
    unit_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    subtotal = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    
    received_quantity = models.IntegerField(
        validators=[MinValueValidator(0)],
        default=0
    )
    received_date = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['item__name']

    def __str__(self):
        return f"{self.item.name} x {self.quantity} @ {self.unit_price}"

    def save(self, *args, **kwargs):
        # Calculate subtotal
        self.subtotal = self.quantity * self.unit_price
        super().save(*args, **kwargs)
        
        # Update purchase order subtotal
        po_subtotal = self.purchase_order.items.aggregate(
            total=models.Sum('subtotal')
        )['total'] or Decimal('0.00')
        self.purchase_order.subtotal = po_subtotal
        self.purchase_order.save()
