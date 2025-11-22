from django.contrib import admin
from unfold.admin import ModelAdmin

from clients.models import Client, ClientComment

@admin.register(Client)
class LeadAdmin(ModelAdmin):
    list_display = ("pk", "name", "email", "description", "created_by", "created_at", "updated_at", "lead")
    search_fields = ("name", "email", "description")
    
@admin.register(ClientComment)
class LeadCommentAdmin(ModelAdmin):
    list_display = ("pk", "content", "team", "created_by", "created_at", "updated_at", "client")
    search_fields = ("content",)