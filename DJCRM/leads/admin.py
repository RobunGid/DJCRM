from django.contrib import admin
from unfold.admin import ModelAdmin
from unfold.contrib.forms.widgets import WysiwygWidget
from django.db import models

from leads.models import Lead

@admin.register(Lead)
class LeadAdmin(ModelAdmin):
    list_display = ("pk", "name", "email", "description", "priority", "status", "created_by", "converted_to_client", "created_at", "updated_at", "client")
    search_fields = ("name", "email", "description", "priority", "status")
    list_filter = ("priority", "status")
    
    formfield_overrides = {
		models.TextField: {
			"widget": WysiwygWidget
		}
	}