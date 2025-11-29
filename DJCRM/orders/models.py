from os import path

from django.db import models
from django.contrib.auth import get_user_model
from django_enum import EnumField
from django.urls import reverse

from teams.models import Team
from products.models import Product

User = get_user_model()

class Order(models.Model):
    class Status(models.TextChoices):
        NEW = "NEW", "New"
        PROCESSING = "PROCESSING", "Processing"
        PENDING_PAYMENT =  "PENDING_PAYMENT", "Pending Payment"
        PAID =  "PAID", "Paid"
        PENDING_SHIPMENT =  "PENDING_SHIPMENT", "Pending Shipment"
        SHIPPED =  "SHIPPED", "Shipped"
        DELIVERED =  "DELIVERED", "Delivered"
        COMPLETED =  "COMPLETED", "Completed"
        CANCELED =  "CANCELED", "Canceled"
        RETURNED = "RETURNED", "Returned"
        
    products = models.ManyToManyField(Product, through="OrderItems")
        
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    status = EnumField(Status, null=False, blank=False, default=Status.NEW)
    team = models.ForeignKey(Team, related_name="orders", on_delete=models.CASCADE)
    
    created_by = models.ForeignKey(User, related_name="orders", on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.pk}: {self.name}'
    
    def get_absolute_url(self):
        return reverse("orders:order_details", kwargs={"pk": self.pk})
    
class OrderItems(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    
class OrderFile(models.Model):
    file = models.FileField(upload_to='order_files')
    
    order = models.ForeignKey(Order, related_name="order_files", on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, related_name="order_files", on_delete=models.CASCADE)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    is_image = models.BooleanField()
    
    def __str__(self):
        return f'@{self.created_by.username}: {self.content}'
    
    def filename(self):
        return path.basename(self.file.name)
    
class OrderComment(models.Model):
    content = models.TextField(blank=True, null=True)
    
    team = models.ForeignKey(Team, related_name="order_comments", on_delete=models.CASCADE)
    order = models.ForeignKey(Order, related_name="comments", on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, related_name="order_comments", on_delete=models.CASCADE)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'@{self.created_by.username}: {self.content}'