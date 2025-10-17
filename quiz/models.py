from django.db import models


class Subject(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Question(models.Model):
    text = models.CharField(max_length=255)
    subject = models.ForeignKey(Subject, null=True, blank=True, on_delete=models.SET_NULL, related_name='questions')

    def __str__(self):
        return self.text


class Choice(models.Model):
    question = models.ForeignKey(Question, related_name='choices', on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.text} ({'correct' if self.is_correct else 'wrong'})"


class TestAttempt(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    started_at = models.DateTimeField()
    finished_at = models.DateTimeField(null=True, blank=True)
    score = models.IntegerField(default=0)
    total = models.IntegerField(default=0)
    subjects = models.CharField(max_length=255, blank=True)  # comma-separated subject names
    questions = models.TextField(blank=True)  # JSON list or comma-separated ids

    def __str__(self):
        return f"{self.user.username} - {self.started_at:%Y-%m-%d %H:%M}"
 

# New model: store contact.html submissions
class ContactSubmission(models.Model):
    name = models.CharField("Name", max_length=150)
    email = models.EmailField("Email")
    subject = models.CharField("Subject", max_length=200, blank=True)
    message = models.TextField("Message")
    submitted_at = models.DateTimeField("Submitted at", auto_now_add=True)
    ip_address = models.GenericIPAddressField("IP address", null=True, blank=True)

    class Meta:
        verbose_name = "Contact submission"
        verbose_name_plural = "Contact submissions"
        ordering = ("-submitted_at",)

    def __str__(self):
        return f"{self.name} <{self.email}> ({self.submitted_at:%Y-%m-%d %H:%M})"



