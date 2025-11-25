from django.contrib.auth import get_user_model
from django.db import models

from teams.models import Team

User = get_user_model()
class Userprofile(models.Model):
    user = models.OneToOneField(User, related_name="userprofile", on_delete=models.CASCADE)
    active_team = models.ForeignKey(Team, related_name="userprofiles", on_delete=models.CASCADE)