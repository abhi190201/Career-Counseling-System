from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from django.core.validators import MinValueValidator, MaxValueValidator

from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


# ✅ Custom User Model
class CustomUser(AbstractUser):
    full_name = models.CharField(max_length=255)
    profile_picture = models.ImageField(
        upload_to='profile_pics/',
        default='profile_pics/default-avatar.jpg',
        blank=True,
        null=True
    )
    tenth_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    twelfth_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    graduation_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    graduation_year = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1950), MaxValueValidator(2100)]
    )
    graduation_stream = models.CharField(max_length=100, null=True, blank=True)
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)
    date_joined = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.username

@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created and not hasattr(instance, 'userprofile'):
        UserProfile.objects.create(user=instance)

class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    other_graduation_stream = models.CharField(max_length=100, blank=True, null=True)

    def is_complete(self):
        required_fields = [
            self.user.full_name,
            self.user.email,
            self.user.tenth_percentage,
            self.user.twelfth_percentage,
            self.user.graduation_percentage,
            self.user.graduation_year,
            self.user.graduation_stream,
            self.user.resume,
        ]
        return all(required_fields)




# ✅ Questionnaire Model


# ✅ Question Model linked to Questionnaire

class InterestQuestion(models.Model):
    question_no = models.CharField(max_length=10, unique=True)
    question_text = models.TextField()

    class Meta:
        db_table = 'interest_questions'  # Custom table name

# models.py
class InterestOption(models.Model):
    option_label = models.CharField(max_length=1)
    option_text = models.TextField()
    question = models.ForeignKey(InterestQuestion, related_name='options', on_delete=models.CASCADE)
    domain = models.ForeignKey('Domain', on_delete=models.CASCADE, null=True)  # Add this line

    class Meta:
        db_table = 'interest_options'


# ✅ Result Model linked to CustomUser

class InterestResult(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Use AUTH_USER_MODEL
    recommended_domains = models.JSONField()  # Storing as JSON to keep domain info
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Interest result for {self.user.username} - {self.timestamp}"

# ✅ Roadmap Model linked to CustomUser and Domain
class Roadmap(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    domain = models.ForeignKey('Domain', on_delete=models.CASCADE)
    level = models.CharField(max_length=20, choices=[
        ('begining', 'Begining'),
        ('intermediate', 'Intermediate'),
        ('expert', 'Expert')
    ])
    generated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} - {self.domain.DomainName} ({self.level})"


# ✅ Course Model
class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    domain = models.CharField(max_length=100)
    link = models.URLField()
    image = models.URLField(blank=True, null=True)  # ✅ Add image URL support

    def __str__(self):
        return self.title




# ✅ Progress Model linked to CustomUser
class Progress(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Use AUTH_USER_MODEL
    profile_complete = models.BooleanField(default=False)
    test_complete = models.BooleanField(default=False)
    roadmap_complete = models.BooleanField(default=False)
    courses_complete = models.BooleanField(default=False)
    domain_complete = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username}'s Progress"


class Domain(models.Model):
    DomainID = models.AutoField(primary_key=True)
    DomainName = models.CharField(max_length=255)

    class Meta:
        db_table = 'domains'

    def __str__(self):
        return self.DomainName



# career/models.py
class DomainModel(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()


# career/models.py
class DomainQuestion(models.Model):
    Domain = models.ForeignKey(Domain, on_delete=models.CASCADE, related_name="questions")  # Foreign key to Domain
    DomainQuestionID = models.AutoField(primary_key=True)
    QuestionNumber = models.IntegerField()
    QuestionText = models.TextField(null=True, blank=True)
    OptionA = models.TextField(null=True, blank=True)
    OptionB = models.TextField(null=True, blank=True)
    OptionC = models.TextField(null=True, blank=True)
    OptionD = models.TextField(null=True, blank=True)
    CorrectAnswer = models.CharField(max_length=1, null=True, blank=True)
    Explanation = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'domainquestions'
        unique_together = ('Domain', 'QuestionNumber')  # Ensure the question number is unique per domain

    def __str__(self):
        return f"{self.Domain.DomainName} Q{self.QuestionNumber}"


class DomainTestResult(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    domain = models.ForeignKey(Domain, on_delete=models.CASCADE)
    score = models.IntegerField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'domain')  # ensures one result per domain per user

    def __str__(self):
        return f"{self.user.username} - {self.domain.DomainName} - {self.score}"

