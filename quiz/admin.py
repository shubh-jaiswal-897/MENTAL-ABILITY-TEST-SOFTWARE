from django.contrib import admin
from .models import (
    Subject, Question, Choice, TestAttempt, 
    ContactSubmission, UserProfile, Contest, 
    GoodieItem, UserGoodieRedemption
)


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 4


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'question_count')
    search_fields = ('name',)

    def question_count(self, obj):
        return obj.questions.count()
    question_count.short_description = "Total Questions"


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    change_list_template = "admin/quiz/question/change_list.html"
    inlines = [ChoiceInline]
    list_display = ('id', 'text', 'subject', 'difficulty', 'choices_count')
    list_filter = ('difficulty', 'subject')
    search_fields = ('text', 'explanation')
    list_editable = ('difficulty', 'subject')
    list_per_page = 25

    def get_urls(self):
        from django.urls import path
        urls = super().get_urls()
        custom_urls = [
            path('ai-generate/', self.admin_site.admin_view(self.ai_generate_view), name='ai_generate_questions'),
        ]
        return custom_urls + urls

    def ai_generate_view(self, request):
        from django.shortcuts import render, redirect
        from django.contrib import messages
        from django.contrib import messages
        from .ai_generator import generate_ai_questions, fetch_internet_questions

        if request.method == 'POST':
            subject_id = request.POST.get('subject')
            difficulty = request.POST.get('difficulty')
            source = request.POST.get('source', 'internet')
            try:
                count = int(request.POST.get('count', 5))
            except Exception:
                count = 5

            if source == 'internet':
                created = fetch_internet_questions(subject_id=subject_id, difficulty=difficulty, count=count)
                messages.success(request, f"🌐 Success! Fetched and imported {len(created)} real questions over the internet!")
            else:
                created = generate_ai_questions(subject_id=subject_id, difficulty=difficulty, count=count)
                messages.success(request, f"🤖 Success! Generated {len(created)} new AI reasoning questions into the database!")

            return redirect('admin:quiz_question_changelist')

        context = {
            **self.admin_site.each_context(request),
            'title': 'AI & Web Question Generator 🤖🌐',
            'subjects': Subject.objects.all(),
            'opts': self.model._meta,
        }
        return render(request, 'admin/quiz/question/ai_generate.html', context)

    def choices_count(self, obj):
        return obj.choices.count()
    choices_count.short_description = "Choices"


@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'question', 'text', 'is_correct')
    list_filter = ('is_correct', 'question__subject')
    search_fields = ('text', 'question__text')
    list_editable = ('is_correct',)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'streak_count', 'total_xp', 'solved_questions_count', 'rank_title', 'last_active_date')
    list_editable = ('streak_count', 'total_xp', 'solved_questions_count')
    search_fields = ('user__username', 'user__email')
    list_filter = ('last_active_date',)


@admin.register(Contest)
class ContestAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'contest_type', 'start_time', 'end_time', 'duration_minutes', 'xp_prize')
    list_filter = ('contest_type', 'start_time')
    search_fields = ('title', 'description')
    filter_horizontal = ('questions',)
    list_editable = ('contest_type', 'duration_minutes', 'xp_prize')


@admin.register(GoodieItem)
class GoodieItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'coin_cost', 'stock', 'icon_class', 'image_path')
    list_editable = ('coin_cost', 'stock', 'icon_class', 'image_path')
    search_fields = ('name', 'description')


@admin.register(UserGoodieRedemption)
class UserGoodieRedemptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'goodie', 'full_name', 'phone_number', 'city', 'pincode', 'status', 'formatted_redeemed_at')
    list_editable = ('status',)
    list_filter = ('status', 'redeemed_at', 'goodie')
    search_fields = ('user__username', 'goodie__name', 'full_name', 'phone_number', 'city', 'pincode', 'shipping_address')
    readonly_fields = ('redeemed_at',)
    fieldsets = (
        ('Order & Customer Overview', {
            'fields': ('user', 'goodie', 'status', 'redeemed_at')
        }),
        ('Shipping Delivery Address', {
            'fields': ('full_name', 'phone_number', 'shipping_address', 'city', 'state', 'pincode')
        }),
    )

    def formatted_redeemed_at(self, obj):
        from django.utils import timezone
        if obj.redeemed_at:
            return timezone.localtime(obj.redeemed_at).strftime('%Y-%m-%d %H:%M:%S IST')
        return "-"
    formatted_redeemed_at.short_description = "Redeemed At"


@admin.register(TestAttempt)
class TestAttemptAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'formatted_started_at', 'formatted_finished_at', 'score', 'total', 'subjects')
    list_filter = ('started_at', 'user')
    search_fields = ('user__username', 'subjects')

    def formatted_started_at(self, obj):
        from django.utils import timezone
        if obj.started_at:
            return timezone.localtime(obj.started_at).strftime('%Y-%m-%d %H:%M:%S IST')
        return "-"
    formatted_started_at.short_description = "Started At"

    def formatted_finished_at(self, obj):
        from django.utils import timezone
        if obj.finished_at:
            return timezone.localtime(obj.finished_at).strftime('%Y-%m-%d %H:%M:%S IST')
        return "-"
    formatted_finished_at.short_description = "Finished At"


@admin.register(ContactSubmission)
class ContactSubmissionAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "email", "subject", "short_message", "formatted_submitted_at", "ip_address")
    search_fields = ("name", "email", "subject", "message")
    list_filter = ("submitted_at",)
    date_hierarchy = "submitted_at"
    readonly_fields = ("submitted_at", "ip_address")
    list_per_page = 25

    def formatted_submitted_at(self, obj):
        from django.utils import timezone
        if obj.submitted_at:
            return timezone.localtime(obj.submitted_at).strftime('%Y-%m-%d %H:%M:%S IST')
        return "-"
    formatted_submitted_at.short_description = "Submitted At"

    def short_message(self, obj):
        return (obj.message[:80] + "…") if len(obj.message) > 80 else obj.message
    short_message.short_description = "Message"
