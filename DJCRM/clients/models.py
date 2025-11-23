from os import path

from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

from teams.models import Team

User = get_user_model()

class Client(models.Model):
    name = models.CharField(max_length = 1023)
    email = models.EmailField()
    description = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(User, related_name="clients", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    team = models.ForeignKey(Team, related_name="clients", on_delete=models.CASCADE)
    
    class Meta:
        ordering = ("name",)
    
    def __str__(self):
        return f'{self.pk}: {self.name}'
    
    def get_absolute_url(self):
        return reverse("clients:client_details", kwargs={"pk": self.pk})
    
    def has_lead(self):
    	return hasattr(self, 'lead') and self.lead is not None
 
class ClientFile(models.Model):
    file = models.FileField(upload_to='client_files')
    
    team = models.ForeignKey(Team, related_name="client_files", on_delete=models.CASCADE)
    client = models.ForeignKey(Client, related_name="files", on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, related_name="client_files", on_delete=models.CASCADE)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    is_image = models.BooleanField()
    
    def __str__(self):
        return f'@{self.created_by.username}: {self.content}'
    
    def filename(self):
        return path.basename(self.file.name)
 
class ClientComment(models.Model):
    content = models.TextField(blank=True, null=True)
    
    team = models.ForeignKey(Team, related_name="client_comments", on_delete=models.CASCADE)
    client = models.ForeignKey(Client, related_name="comments", on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, related_name="client_comments", on_delete=models.CASCADE)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)