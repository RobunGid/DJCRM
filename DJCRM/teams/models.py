from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()
    
class Plan(models.Model):
    name = models.CharField(max_length=63)
    price = models.IntegerField()
    description = models.TextField(blank=True, null=True)
    max_leads = models.IntegerField()
    max_clients = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'{self.pk}: {self.name}'
    
class Team(models.Model):
    name = models.CharField(max_length=127)
    members = models.ManyToManyField(User, related_name="teams")
    created_by = models.ForeignKey(User, related_name="created_teams", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, related_name="teams", default=1)
    
    def __str__(self):
        return f'{self.pk}: {self.name}'