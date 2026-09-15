from django.db import models
from django.conf import settings

class StudyMaterial(models.Model):
    """User uploaded study material files."""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='study_materials')
    title = models.CharField(max_length=255)
    file_url = models.URLField(max_length=1000, blank=True, null=True, help_text="Direct URL to the file in Supabase Storage")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.user.username})"

class Exam(models.Model):
    """Exam generated from a StudyMaterial instance."""
    material = models.ForeignKey(StudyMaterial, on_delete=models.CASCADE, related_name='exams')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    score = models.IntegerField(default=0)
    total = models.IntegerField(default=0)

    def __str__(self):
        return f"Exam #{self.id} for {self.user.username} on {self.material.title}" 

class ExamQuestion(models.Model):
    """Individual MCQ generated for an exam."""
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField()
    choice_a = models.CharField(max_length=255)
    choice_b = models.CharField(max_length=255)
    choice_c = models.CharField(max_length=255)
    choice_d = models.CharField(max_length=255)
    correct_choice = models.CharField(max_length=1, choices=[('A','A'),('B','B'),('C','C'),('D','D')])
    user_answer = models.CharField(max_length=1, null=True, blank=True)

    def is_correct(self):
        return self.user_answer == self.correct_choice
