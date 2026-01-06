from django.db import models

class Plan(models.Model):
    name = models.CharField(max_length=63)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    description = models.TextField(blank=True, null=True)
    max_leads = models.IntegerField()
    max_clients = models.IntegerField()
    max_products = models.IntegerField()
    max_orders = models.IntegerField()
    max_order_items = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'{self.pk}: {self.name}'