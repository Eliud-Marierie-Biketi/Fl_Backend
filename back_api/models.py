from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from datetime import timedelta, date
from django.conf import settings

# Teacher model with subscription functionality
class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="teacher_profile")
    email = models.EmailField(max_length=100)
    school_name = models.CharField(max_length=100, blank=True)
    mobile_phone = models.CharField(
        max_length=10,  # Kenyan phone numbers are 10 digits without country code
        validators=[RegexValidator(regex=r'^\d{10}$', message="Phone number must be 10 digits.")]
    )
    free_downloads_remaining = models.IntegerField(default=10)
    paid_downloads = models.IntegerField(default=0)
    is_premium = models.BooleanField(default=False)
    subscription_start_date = models.DateField(default=date.today)
    subscription_end_date = models.DateField(default=date.today() + timedelta(days=36))

    def save(self, *args, **kwargs):
        # Expire premium if the subscription end date has passed
        if date.today() > self.subscription_end_date:
            self.is_premium = False
        super().save(*args, **kwargs)

    def start_premium_subscription(self, days=365):
        """Activate premium subscription for a specified number of days (default 1 year)."""
        self.is_premium = True
        self.subscription_start_date = date.today()
        self.subscription_end_date = date.today() + timedelta(days=days)
        self.save()
    
    def is_subscription_active(self):
        """Check if the subscription is currently active."""
        return self.is_premium and self.subscription_end_date >= date.today()

    def __str__(self):
        return f"Teacher {self.user.username}"

# Profile model for additional user information
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bio = models.TextField(default="No bio provided")
    avatar = models.ImageField(upload_to='avatars', default='no_picture.png')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Profile of {self.user.username}"

# Class model representing a class taught by a teacher
class Class(models.Model):
    name = models.CharField(max_length=100)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='classes')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name} (Teacher: {self.teacher.user.username})'

# Subject model representing subjects in a school
class Subject(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# Exam model representing an exam for a specific class
class Exam(models.Model):
    class_instance = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='exams')
    name = models.CharField(max_length=100)  # e.g., "End Term Exam"
    date = models.DateField(auto_now_add=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} - {self.class_instance.name} ({self.date})"

# ExamSubject model linking exams to subjects with a max score
class ExamSubject(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='exam_subjects')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    max_marks = models.FloatField(null=True)

    def __str__(self):
        return f"{self.subject.name} for {self.exam.name}"

# Student model representing students in a class
class Student(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    assessment_no = models.CharField(max_length=100, unique=True)
    registration_no = models.CharField(max_length=100, blank=True)
    age = models.IntegerField(blank=True, null=True)
    gender = models.CharField(max_length=10, choices=[('M', 'Male'), ('F', 'Female')])
    class_instance = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='students')
    subjects = models.ManyToManyField(Subject, related_name='students')

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

# Score model representing scores for individual exam subjects per student
class Score(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='scores')
    exam_subject = models.ForeignKey(ExamSubject, on_delete=models.CASCADE, related_name='scores')
    marks_obtained = models.FloatField(null=True)

    def __str__(self):
        return f"{self.student} - {self.exam_subject.subject.name} - {self.marks_obtained}"

# Result model to store final term and year results per student for each subject
class Result(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='results')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    term = models.IntegerField()
    year = models.IntegerField()
    score = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        unique_together = ('student', 'subject', 'term', 'year')

# StudentReport model for storing term reports per student
class StudentReport(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='reports')
    term = models.IntegerField()
    year = models.IntegerField()
    comments = models.TextField()
    rank = models.IntegerField()  # Calculated based on scores
    average_score = models.DecimalField(max_digits=5, decimal_places=2)

# ClassPerformance model for overall class performance per term
class ClassPerformance(models.Model):
    school_class = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='performances')
    term = models.IntegerField()
    year = models.IntegerField()
    average_score = models.DecimalField(max_digits=5, decimal_places=2)
    top_performer = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True, related_name="top_performer_records")

# Subscription model for teacher subscriptions
class Subscription(models.Model):
    PLAN_CHOICES = [
        ('basic', 'Basic'),
        ('premium', 'Premium'),
    ]
    teacher = models.OneToOneField(User, on_delete=models.CASCADE)
    plan = models.CharField(max_length=10, choices=PLAN_CHOICES, default='basic')
    status = models.CharField(max_length=20, choices=[('active', 'Active'), ('inactive', 'Inactive')])
    expiry_date = models.DateField()

# PaymentRecord model to store payment records
class PaymentRecord(models.Model):
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_id = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=20, choices=[('completed', 'Completed'), ('failed', 'Failed')])
    timestamp = models.DateTimeField(auto_now_add=True)
