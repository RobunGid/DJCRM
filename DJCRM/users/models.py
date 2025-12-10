from django.db import models
from django.conf import settings

class Userprofile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name="userprofile", on_delete=models.CASCADE)
    active_team = models.ForeignKey("teams.Team", related_name="userprofiles", on_delete=models.CASCADE)
    
    def __str__(self):
        return f'@{self.user.username}'