from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone


class Supplier(models.Model):
    """
    Model representing a supplier/vendor in the system.
    Tracks supplier information and performance metrics.
    """
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=50, unique=True)
    contact_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()
    website = models.URLField(blank=True)
    tax_id = models.CharField(max_length=50, blank=True)
    
    # Performance metrics
    reliability_rating = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        default=5.00
    )
    average_lead_time = models.IntegerField(
        help_text="Average lead time in days",
        default=0
    )
    on_time_delivery_rate = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        default=100.00,
        help_text="Percentage of on-time deliveries"
    )
    
    # Status and metadata
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.code})"
    
    def update_performance_metrics(self):
        """Update supplier performance metrics based on order history"""
        from .purchase_order import PurchaseOrder
        
        # Calculate metrics based on last 6 months of orders
        six_months_ago = timezone.now() - timezone.timedelta(days=180)
        recent_orders = PurchaseOrder.objects.filter(
            supplier=self,
            created_at__gte=six_months_ago
        )
        
        if recent_orders.exists():
            # Calculate on-time delivery rate
            on_time_orders = recent_orders.filter(
                actual_delivery_date__lte=models.F('expected_delivery_date')
            ).count()
            total_orders = recent_orders.count()
            self.on_time_delivery_rate = (on_time_orders / total_orders) * 100
            
            # Calculate average lead time
            lead_times = recent_orders.exclude(
                actual_delivery_date=None
            ).annotate(
                lead_time=models.ExpressionWrapper(
                    models.F('actual_delivery_date') - models.F('order_date'),
                    output_field=models.DurationField()
                )
            )
            if lead_times.exists():
                avg_lead_time = lead_times.aggregate(
                    avg_lead=models.Avg('lead_time')
                )['avg_lead']
                self.average_lead_time = avg_lead_time.days
            
            # Update reliability rating based on delivery rate
            self.reliability_rating = min(5.0, self.on_time_delivery_rate / 20)
            
            self.save()


class SupplierContact(models.Model):
    """
    Additional contacts for a supplier beyond the primary contact.
    """
    supplier = models.ForeignKey(
        Supplier,
        on_delete=models.CASCADE,
        related_name='additional_contacts'
    )
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    is_primary = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-is_primary', 'name']

    def __str__(self):
        return f"{self.name} ({self.role}) - {self.supplier.name}"
    
    def save(self, *args, **kwargs):
        if self.is_primary:
            # Ensure only one primary contact per supplier
            SupplierContact.objects.filter(
                supplier=self.supplier,
                is_primary=True
            ).exclude(id=self.id).update(is_primary=False)
        super().save(*args, **kwargs)
