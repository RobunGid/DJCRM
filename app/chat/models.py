from django.db import models
from django.conf import settings
from django.core.validators import MinLengthValidator
from django.db.models import Q

from teams.models import Team

class Message(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="sender", on_delete=models.CASCADE)
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="receiver", on_delete=models.CASCADE, null=True, blank=True)
    team = models.ForeignKey(Team, related_name="team", null=True, blank=True, on_delete=models.CASCADE)
    text = models.TextField(max_length=1024, validators=(MinLengthValidator(1),))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ("created_at",)
        constraints = [
            models.CheckConstraint(
                name="null_receiver_only_if_team_exists",
                check=(
                    Q(team_id__isnull=False) |
                    Q(receiver_id__isnull=False)
                )
            )
        ]
    
    def __str__(self):
        sender = getattr(self.sender, "user", None)
        username = getattr(sender, "username", "unknown")
        return f"{username}: {self.text}"