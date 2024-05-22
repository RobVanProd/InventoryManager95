from django.db import models
from django.contrib.auth.models import User

class Warehouse(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class SubWarehouse(models.Model):
    name = models.CharField(max_length=100)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name='subwarehouses')
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='subwarehouse')

    def __str__(self):
        return self.name

class InventoryItem(models.Model):
    name = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name='items', blank=True, null=True)
    subwarehouse = models.ForeignKey(SubWarehouse, on_delete=models.CASCADE, related_name='items', blank=True, null=True)

    def __str__(self):
        return self.name
