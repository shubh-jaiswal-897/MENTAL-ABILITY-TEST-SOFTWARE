from django.db import models


class Subject(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Question(models.Model):
    EASY = 'EASY'
    MEDIUM = 'MEDIUM'
    HARD = 'HARD'
    DIFFICULTY_CHOICES = [
        (EASY, 'Easy'),
        (MEDIUM, 'Medium'),
        (HARD, 'Hard'),
    ]

    text = models.CharField(max_length=255)
    subject = models.ForeignKey(Subject, null=True, blank=True, on_delete=models.SET_NULL, related_name='questions')
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default=MEDIUM)
    explanation = models.TextField(blank=True, help_text="Detailed step-by-step logic solution")

    def __str__(self):
        return f"[{self.difficulty}] {self.text}"


class Choice(models.Model):
    question = models.ForeignKey(Question, related_name='choices', on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.text} ({'correct' if self.is_correct else 'wrong'})"


class UserProfile(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE, related_name='profile')
    streak_count = models.IntegerField(default=0)
    last_active_date = models.DateField(null=True, blank=True)
    total_xp = models.IntegerField(default=0)
    solved_questions_count = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username}'s Profile (Streak: {self.streak_count}🔥, XP: {self.total_xp})"

    @property
    def rank_title(self):
        if self.total_xp >= 1000:
            return "Grandmaster 👑"
        elif self.total_xp >= 500:
            return "Mind Master 🧠"
        elif self.total_xp >= 200:
            return "Aptitude Scholar 🎓"
        elif self.total_xp >= 50:
            return "Problem Solver ⚡"
        else:
            return "Novice Explorer"


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

    @property
    def percentage(self):
        if self.total > 0:
            return round((self.score / self.total) * 100, 1)
        return 0.0

    @property
    def is_perfect(self):
        return self.total > 0 and self.score == self.total

    @property
    def is_passed(self):
        return self.percentage >= 33.0

    @property
    def status_label(self):
        if self.is_perfect:
            return "PERFECT 🎯"
        elif self.is_passed:
            return "PASSED ⚡"
        else:
            return "TRY AGAIN"


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


class Contest(models.Model):
    WEEKLY = 'WEEKLY'
    MONTHLY = 'MONTHLY'
    CONTEST_TYPES = [
        (WEEKLY, 'Weekly Contest'),
        (MONTHLY, 'Monthly Championship'),
    ]

    title = models.CharField(max_length=200)
    contest_type = models.CharField(max_length=10, choices=CONTEST_TYPES, default=WEEKLY)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    duration_minutes = models.IntegerField(default=60)
    questions = models.ManyToManyField(Question, related_name='contests', blank=True)
    xp_prize = models.IntegerField(default=200)

    class Meta:
        ordering = ('-start_time',)

    def __str__(self):
        return f"[{self.get_contest_type_display()}] {self.title}"


class GoodieItem(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField()
    coin_cost = models.IntegerField(help_text="XP / Goodies Coins required to redeem")
    icon_class = models.CharField(max_length=100, default="fas fa-gift")
    image_path = models.CharField(max_length=255, blank=True, null=True)
    stock = models.IntegerField(default=50)

    def __str__(self):
        return f"{self.name} ({self.coin_cost} XP)"


class UserGoodieRedemption(models.Model):
    STATUS_CHOICES = [
        ('Pending Processing', 'Pending Processing'),
        ('Shipped 🚚', 'Shipped 🚚'),
        ('Delivered 🎉', 'Delivered 🎉'),
        ('Cancelled ❌', 'Cancelled ❌'),
    ]

    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='redemptions')
    goodie = models.ForeignKey(GoodieItem, on_delete=models.CASCADE, related_name='redemptions')
    full_name = models.CharField("Full Name", max_length=150, blank=True)
    phone_number = models.CharField("Phone Number", max_length=20, blank=True)
    shipping_address = models.TextField("Shipping Address", blank=True)
    city = models.CharField("City", max_length=100, blank=True)
    state = models.CharField("State", max_length=100, blank=True)
    pincode = models.CharField("Pincode / Zip", max_length=20, blank=True)
    redeemed_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField("Order Status", max_length=50, choices=STATUS_CHOICES, default="Pending Processing")

    class Meta:
        verbose_name = "Goodie Order / Redemption"
        verbose_name_plural = "Goodie Orders & Redemptions"
        ordering = ('-redeemed_at',)

    def __str__(self):
        return f"Order #{self.id}: {self.user.username} -> {self.goodie.name} ({self.status})"

    def save(self, *args, **kwargs):
        if self.pk:
            try:
                old_instance = UserGoodieRedemption.objects.get(pk=self.pk)
                # Case 1: Status changing TO Cancelled ❌ -> Refund XP and restore stock
                if old_instance.status != 'Cancelled ❌' and self.status == 'Cancelled ❌':
                    if hasattr(self.user, 'profile'):
                        self.user.profile.total_xp += self.goodie.coin_cost
                        self.user.profile.save()
                    self.goodie.stock += 1
                    self.goodie.save()

                # Case 2: Status changing FROM Cancelled ❌ back to active status -> Re-deduct XP and decrement stock
                elif old_instance.status == 'Cancelled ❌' and self.status != 'Cancelled ❌':
                    if hasattr(self.user, 'profile'):
                        self.user.profile.total_xp = max(0, self.user.profile.total_xp - self.goodie.coin_cost)
                        self.user.profile.save()
                    self.goodie.stock = max(0, self.goodie.stock - 1)
                    self.goodie.save()
            except UserGoodieRedemption.DoesNotExist:
                pass
        super().save(*args, **kwargs)





