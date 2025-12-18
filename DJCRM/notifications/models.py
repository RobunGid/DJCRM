from django.db import models

from django.conf import settings

class NotificationType(models.Model):
    name = models.CharField(max_length=127)

class Notification(models.Model):
    content = models.TextField(blank=True)

    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="notifications", on_delete=models.CASCADE)
    notification_type = models.ForeignKey(NotificationType, related_name="notifications", on_delete=models.DO_NOTHING)
    is_read = models.BooleanField()
    read_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'#{self.pk}: {self.content}'