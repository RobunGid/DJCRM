from os import path

from django.db import models
from django.contrib.auth import get_user_model
from django_enum import EnumField
from django.urls import reverse

from teams.models import Team

User = get_user_model()

class Product(models.Model):
    class Status(models.TextChoices):
        DRAFT = "DRAFT", "Draft"
        OUT_OF_STOCK = "OUT_OF_STOCK", "Out of Stock"
        ARCHIVED = "ARCHIVED", "Archived"
        ACTIVE = "ACTIVE", "Active"
        INACTIVE = "INACTIVE", "Inactive"
        
    name = models.CharField(max_length=63)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    stock_quantity = models.IntegerField()
    
    status = EnumField(Status, null=False, blank=False, default=Status.DRAFT)
    weight = models.IntegerField()
    team = models.ForeignKey(Team, related_name="products", on_delete=models.CASCADE)
    
    created_by = models.ForeignKey(User, related_name="products", on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.pk}: {self.name}'
    
    def get_absolute_url(self):
        return reverse("products:product_details", kwargs={"pk": self.pk})
    
class ProductFile(models.Model):
    file = models.FileField(upload_to='product_files')
    
    product = models.ForeignKey(Product, related_name="product_files", on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, related_name="product_files", on_delete=models.CASCADE)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    is_image = models.BooleanField()
    
    def __str__(self):
        return f'@{self.created_by.username}: {self.content}'
    
    def filename(self):
        return path.basename(self.file.name)
    
class ProductComment(models.Model):
    content = models.TextField(blank=True, null=True)
    
    team = models.ForeignKey(Team, related_name="product_comments", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name="comments", on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, related_name="product_comments", on_delete=models.CASCADE)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'@{self.created_by.username}: {self.content}'