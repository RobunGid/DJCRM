from django.contrib import admin
from unfold.admin import ModelAdmin

from teams.models import Team

@admin.register(Team)
class LeadAdmin(ModelAdmin):
    list_display = ("pk", "name", "created_by", "created_at", "updated_at",)
    search_fields = ("name", "members")