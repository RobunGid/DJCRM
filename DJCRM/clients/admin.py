from django.contrib import admin
from unfold.admin import ModelAdmin

from clients.models import Client

@admin.register(Client)
class LeadAdmin(ModelAdmin):
    list_display = ("pk", "name", "email", "description", "created_by", "created_at", "updated_at", "lead")
    search_fields = ("name", "email", "description")