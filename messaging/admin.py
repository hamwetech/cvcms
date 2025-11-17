from django.contrib import admin
from messaging.models import SMSLog


@admin.register(SMSLog)
class SMSLogAdmin(admin.ModelAdmin):
    change_list_template = "admin/messaging/sms_message_change_list.html"
    list_display = ("phone", "message", "status", "created_at")
    search_fields = ("phone", "message")
    list_filter = ("status", "created_at")

    def has_add_permission(self, request):
        return False  # Completely disables the ADD button
