from django.contrib import admin
from .models import Question, Choice, ContactSubmission


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 1


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]
    list_display = ('text', 'subject')


from .models import Subject


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name',)

from .models import TestAttempt


@admin.register(TestAttempt)
class TestAttemptAdmin(admin.ModelAdmin):
    list_display = ('user', 'started_at', 'finished_at', 'score', 'total')
    readonly_fields = ('started_at', 'finished_at', 'score', 'total')


@admin.register(ContactSubmission)
class ContactSubmissionAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "subject", "short_message", "submitted_at", "ip_address")
    search_fields = ("name", "email", "subject", "message")
    list_filter = ("submitted_at",)
    date_hierarchy = "submitted_at"
    readonly_fields = ("submitted_at", "ip_address")
    list_per_page = 25

    def short_message(self, obj):
        return (obj.message[:80] + "…") if len(obj.message) > 80 else obj.message
    short_message.short_description = "Message"
