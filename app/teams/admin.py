from django.contrib import admin
from unfold.admin import ModelAdmin

from teams.models import Team
from teams.models import Plan

@admin.register(Team)
class LeadAdmin(ModelAdmin):
    list_display = ("pk", "name", "created_by", "created_at", "updated_at",)
    search_fields = ("name", "members")
    
@admin.register(Plan)
class PlanAdmin(ModelAdmin):
    list_display = ("pk", "name", "price", "description", "max_leads", "max_clients", "created_at", "updated_at",)
    search_fields = ("name",)