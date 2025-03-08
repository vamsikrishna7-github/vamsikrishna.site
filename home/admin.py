from django.contrib import admin
from home.models import *

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone", "title", "project_type", "created_at")
    search_fields = ("name", "email", "title")