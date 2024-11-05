from rest_framework import serializers
from .models import (
    Teacher, Profile, Class, Subject, Exam, ExamSubject,
    Student, Score, Result, StudentReport, ClassPerformance,
    Subscription, PaymentRecord
)
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    school_name = serializers.CharField(max_length=100, required=False)
    mobile_phone = serializers.CharField(max_length=10, required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'school_name', 'mobile_phone')

    def create(self, validated_data):
        # Extract teacher fields from the validated data
        school_name = validated_data.pop('school_name', '')
        mobile_phone = validated_data.pop('mobile_phone', '')

        # Create User instance
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()

        # Create Teacher instance
        Teacher.objects.create(
            user=user,
            school_name=school_name,
            mobile_phone=mobile_phone
        )
        return user
    
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        user = authenticate(username=username, password=password)
        if user is None:
            raise serializers.ValidationError("Invalid username or password.")
        
        return attrs    
# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

# Teacher Serializer
class TeacherSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Teacher
        fields = [
            'id', 'user', 'email', 'school_name', 'mobile_phone',
            'free_downloads_remaining', 'paid_downloads', 'is_premium',
            'subscription_start_date', 'subscription_end_date'
        ]

# Profile Serializer
class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = ['id', 'user', 'bio', 'avatar', 'created', 'updated']

# Class Serializer
class ClassSerializer(serializers.ModelSerializer):
    teacher = TeacherSerializer(read_only=True)

    class Meta:
        model = Class
        fields = ['id', 'name', 'teacher', 'created', 'updated']

# Subject Serializer
class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['id', 'name']

# Exam Serializer
class ExamSerializer(serializers.ModelSerializer):
    class_instance = ClassSerializer(read_only=True)
    teacher = TeacherSerializer(read_only=True)

    class Meta:
        model = Exam
        fields = ['id', 'class_instance', 'name', 'date', 'teacher']

# ExamSubject Serializer
class ExamSubjectSerializer(serializers.ModelSerializer):
    exam = ExamSerializer(read_only=True)
    subject = SubjectSerializer(read_only=True)

    class Meta:
        model = ExamSubject
        fields = ['id', 'exam', 'subject', 'max_marks']

# Student Serializer
class StudentSerializer(serializers.ModelSerializer):
    class_instance = ClassSerializer(read_only=True)
    subjects = SubjectSerializer(many=True, read_only=True)

    class Meta:
        model = Student
        fields = [
            'id', 'first_name', 'last_name', 'assessment_no', 'registration_no',
            'age', 'gender', 'class_instance', 'subjects'
        ]

# Score Serializer
class ScoreSerializer(serializers.ModelSerializer):
    student = StudentSerializer(read_only=True)
    exam_subject = ExamSubjectSerializer(read_only=True)

    class Meta:
        model = Score
        fields = ['id', 'student', 'exam_subject', 'marks_obtained']

# Result Serializer
class ResultSerializer(serializers.ModelSerializer):
    student = StudentSerializer(read_only=True)
    subject = SubjectSerializer(read_only=True)

    class Meta:
        model = Result
        fields = ['id', 'student', 'subject', 'term', 'year', 'score']

# StudentReport Serializer
class StudentReportSerializer(serializers.ModelSerializer):
    student = StudentSerializer(read_only=True)

    class Meta:
        model = StudentReport
        fields = [
            'id', 'student', 'term', 'year', 'comments', 'rank', 'average_score'
        ]

# ClassPerformance Serializer
class ClassPerformanceSerializer(serializers.ModelSerializer):
    school_class = ClassSerializer(read_only=True)
    top_performer = StudentSerializer(read_only=True)

    class Meta:
        model = ClassPerformance
        fields = [
            'id', 'school_class', 'term', 'year', 'average_score', 'top_performer'
        ]

# Subscription Serializer
class SubscriptionSerializer(serializers.ModelSerializer):
    teacher = UserSerializer(read_only=True)

    class Meta:
        model = Subscription
        fields = ['id', 'teacher', 'plan', 'status', 'expiry_date']

# PaymentRecord Serializer
class PaymentRecordSerializer(serializers.ModelSerializer):
    teacher = UserSerializer(read_only=True)

    class Meta:
        model = PaymentRecord
        fields = [
            'id', 'teacher', 'amount', 'transaction_id', 'status', 'timestamp'
        ]
