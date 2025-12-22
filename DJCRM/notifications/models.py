from django.db import models
from django.conf import settings
from django_enum import EnumField

from teams.models import Team

class Notification(models.Model):
    class Status(models.TextChoices):
        NOT_READ = "NOT_READ", "Not read"
        READ = "READ", "Read"
        HIDDEN = "HIDDEN", "Hidden"
        DELETED = "DELETED", "Deleted"
        FAILED = "FAILED", "Failed"
    title = models.CharField(max_length=63)
    content = models.TextField(blank=True)

    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="notifications", on_delete=models.CASCADE)
    status = EnumField(Status, null=False, blank=False, default=Status.NOT_READ)
    is_read = models.BooleanField()
    read_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ("is_read", "updated_at")
    
    def __str__(self):
        return f'#{self.pk}: {self.content}'
    
class TeamInvitation(models.Model):
    class Status(models.TextChoices):
        NOT_READ = "NOT_READ", "Not read"
        READ = "READ", "Read"
        ACCEPTED = "ACCEPTED", "Accepted"
        DECLINED = "DECLINED", "Declined"
        EXPIRED = "EXPIRED", "Expired"
        CANCELED = "CANCELED", "Canceled"
        
    team = models.ForeignKey(Team, related_name="invitations", on_delete=models.CASCADE)
    status = EnumField(Status, null=False, blank=False, default=Status.NOT_READ)
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="team_invitations", on_delete=models.CASCADE)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)