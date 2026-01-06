from django.db import models
from django.conf import settings

from plans.models import Plan
    
class Team(models.Model):
    name = models.CharField(max_length=127)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="teams")
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="created_teams", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, related_name="teams", default=1)
    
    def __str__(self):
        return f'{self.pk}: {self.name}'