from django.contrib import admin

from .models import Ticket
@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ("title", "description", "status", "priority", "updated_at", "created_at")
    list_filter = ("status", "priority")
    search_fields = ("title", "description")
    readonly_fields = ("updated_at", "created_at",)
