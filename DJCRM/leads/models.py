from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django_enum import EnumField

from clients.models import Client
from teams.models import Team

class NotClientsManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(converted_to_client=False)

User = get_user_model()

class Lead(models.Model):
    class Priority(models.IntegerChoices):
        LOW = 10, 'Low'
        MEDIUM = 20, 'Medium'
        HIGH = 30, 'High'
    class Status(models.TextChoices):
        NEW = "NEW", "New"
        CONTACTED = "CONTACTED", "Contacted"
        WON = "WON", "Won"
        LOST = "LOST", "Lost"
    
    name = models.CharField(max_length = 1023)
    email = models.EmailField()
    description = models.TextField(blank=True, null=True)
    priority = EnumField(Priority, null=False, blank=False, default=Priority.MEDIUM)
    status = EnumField(Status, null=False, blank=False, default=Status.NEW)
    created_by = models.ForeignKey(User, related_name="leads", on_delete=models.CASCADE)
    converted_to_client = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    client = models.OneToOneField(Client, on_delete=models.SET_NULL, null=True, blank=True)
    team = models.ForeignKey(Team, related_name="leads", on_delete=models.CASCADE)
    
    objects = models.Manager()
    not_clients = NotClientsManager()
    
    def __str__(self):
        return f'{self.pk}: {self.name}'
    
    def get_absolute_url(self):
        return reverse("leads:lead_details", kwargs={"pk": self.pk})
    