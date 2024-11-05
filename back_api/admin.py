from django.contrib import admin
from .models import (
    Teacher, Profile, Class, Subject, Exam, ExamSubject,
    Student, Score, Result, StudentReport, ClassPerformance,
    Subscription, PaymentRecord
)

# Registering models with the admin site
admin.site.register(Teacher)
admin.site.register(Profile)
admin.site.register(Class)
admin.site.register(Subject)
admin.site.register(Exam)
admin.site.register(ExamSubject)
admin.site.register(Student)
admin.site.register(Score)
admin.site.register(Result)
admin.site.register(StudentReport)
admin.site.register(ClassPerformance)
admin.site.register(Subscription)
admin.site.register(PaymentRecord)
