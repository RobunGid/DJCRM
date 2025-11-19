from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()

class Client(models.Model):
    name = models.CharField(max_length = 1023)
    email = models.EmailField()
    description = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(User, related_name="clients", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'{self.pk}: {self.name}'
    
    def get_absolute_url(self):
        return reverse("clients:client_details", kwargs={"pk": self.pk})
    
    def has_lead(self):
    	return hasattr(self, 'lead') and self.lead is not None