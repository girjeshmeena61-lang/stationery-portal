from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

class Inventory(models.Model):
    item_name = models.CharField(max_length=100)
    available_qty = models.IntegerField(default=0)
    minimum_qty = models.IntegerField(default=0)
    unit = models.CharField(max_length=20)

    def __str__(self):
        return self.item_name


class Requisition(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
        ('Partial', 'Partial Approved'),
    ]

    DEPARTMENT_CHOICES = [
        ('HR', 'HR'),
        ('Finance', 'Finance'),
        ('IT', 'IT'),
        ('Admin', 'Admin'),
        ('Operations', 'Operations'),
    ]

    item = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    requested_qty = models.IntegerField()
    approved_qty = models.IntegerField(default=0)
    reason = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Pending'
    )

    requested_by = models.CharField(max_length=100)

    department = models.CharField(
        max_length=20,
        choices=DEPARTMENT_CHOICES,
        default='HR'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.item} - {self.requested_by}"