from django.contrib import admin
from .models import ContactSubmission

# ...existing admin registrations (if any)...

@admin.register(ContactSubmission)
class ContactSubmissionAdmin(admin.ModelAdmin):
	list_display = ("name", "email", "subject", "short_message", "submitted_at", "ip_address")
	list_filter = ("submitted_at",)
	search_fields = ("name", "email", "subject", "message")
	date_hierarchy = "submitted_at"
	list_per_page = 25
	readonly_fields = ("submitted_at", "ip_address")

	def short_message(self, obj):
		return (obj.message[:80] + "…") if len(obj.message) > 80 else obj.message
	short_message.short_description = "Message"
