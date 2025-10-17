import uuid

from django.db import models
from django.contrib.auth.models import User

class Supplier(models.Model):
    name = models.CharField(max_length=255)
    contact_person = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)

    def __str__(self):
        return self.name


class MaterialCategory(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Material(models.Model):
    name = models.CharField(max_length=255)
    sku = models.CharField(max_length=100, unique=True)
    category = models.ForeignKey(MaterialCategory, on_delete=models.SET_NULL, null=True, related_name='materials')
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, related_name='materials')
    quantity = models.PositiveIntegerField(default=0)
    reorder_level = models.PositiveIntegerField(default=10)
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def is_low_stock(self):
        return self.quantity <= self.reorder_level

    def __str__(self):
        return f"{self.name} ({self.sku})"

    @property
    def total_value(self):
        return self.quantity * self.unit_cost


class StockTransaction(models.Model):
    material = models.ForeignKey(Material, on_delete=models.CASCADE, related_name='stock_transactions')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    change_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    timestamp = models.DateTimeField(auto_now_add=True)
    note = models.TextField(blank=True)

    def __str__(self):
        return f"{self.material.name} {self.change_amount:+}"


class PurchaseOrder(models.Model):
    order_number = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    materials = models.ManyToManyField(Material, related_name='purchase_orders')
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    ordered_at = models.DateTimeField(auto_now_add=True)
    received = models.BooleanField(default=False)

    def __str__(self):
        return f"PO-{self.order_number}"


class MaterialAuditLog(models.Model):
    class ActionType(models.TextChoices):
        CREATE = 'CREATE', 'Create'
        UPDATE = 'UPDATE', 'Update'
        DELETE = 'DELETE', 'Delete'
        STOCK_ADJUST = 'STOCK_ADJUST', 'Stock Adjust'
        RECEIVE_ORDER = 'RECEIVE_ORDER', 'Receive Order'

    material = models.ForeignKey(Material, on_delete=models.CASCADE, related_name='audit_logs')
    action = models.CharField(choices=ActionType.choices, max_length=30)
    details = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.material.name} - {self.get_action_display()}"
