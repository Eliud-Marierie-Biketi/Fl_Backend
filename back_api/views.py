from rest_framework import viewsets, generics, permissions, status
from rest_framework.permissions import IsAuthenticated
from .models import (
    Teacher, Profile, Class, Subject, Exam, ExamSubject,
    Student, Score, Result, StudentReport, ClassPerformance,
    Subscription, PaymentRecord
)
from .serializers import (
    LoginSerializer, TeacherSerializer, ProfileSerializer, ClassSerializer, SubjectSerializer,
    ExamSerializer, ExamSubjectSerializer, StudentSerializer, ScoreSerializer,
    ResultSerializer, StudentReportSerializer, ClassPerformanceSerializer,
    SubscriptionSerializer, PaymentRecordSerializer, UserRegistrationSerializer
)
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status


# User Registration View
class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]  # Allow any user to register


# Login View
class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]  # Allow any user to access this endpoint

    def post(self, request, *args, **kwargs):
        # Serialize and validate the request data
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # No need to authenticate here, the serializer has already handled that
        user = serializer.validated_data['user']
        token = serializer.validated_data['token']

        # Return the response with the token and user details
        return Response({
            'token': token,
            'user_id': user.id,
            'username': user.username,
        }, status=status.HTTP_200_OK)
 
# Teacher ViewSet
# Custom permission to allow only admin or the owner to access data
class IsAdminOrOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or obj.user == request.user


# Teacher ViewSet
class TeacherViewSet(viewsets.ModelViewSet):
    serializer_class = TeacherSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:  # Admin access
            return Teacher.objects.all()
        return Teacher.objects.filter(user=self.request.user)


# Profile ViewSet
class ProfileViewSet(viewsets.ModelViewSet):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:  # Admin access
            return Profile.objects.all()
        return Profile.objects.filter(user=self.request.user)


# Class ViewSet
class ClassViewSet(viewsets.ModelViewSet):
    serializer_class = ClassSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Class.objects.all()
        return Class.objects.filter(teacher__user=self.request.user)


# Subject ViewSet
class SubjectViewSet(viewsets.ModelViewSet):
    serializer_class = SubjectSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Subject.objects.all()


# Exam ViewSet
class ExamViewSet(viewsets.ModelViewSet):
    serializer_class = ExamSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Exam.objects.all()
        return Exam.objects.filter(teacher__user=self.request.user)


# ExamSubject ViewSet
class ExamSubjectViewSet(viewsets.ModelViewSet):
    serializer_class = ExamSubjectSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return ExamSubject.objects.all()
        return ExamSubject.objects.filter(exam__teacher__user=self.request.user)


# Student ViewSet
class StudentViewSet(viewsets.ModelViewSet):
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Student.objects.all()
        return Student.objects.filter(class_instance__teacher__user=self.request.user)


# Score ViewSet
class ScoreViewSet(viewsets.ModelViewSet):
    serializer_class = ScoreSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Score.objects.all()
        return Score.objects.filter(student__class_instance__teacher__user=self.request.user)


# Result ViewSet
class ResultViewSet(viewsets.ModelViewSet):
    serializer_class = ResultSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Result.objects.all()
        return Result.objects.filter(student__class_instance__teacher__user=self.request.user)


# StudentReport ViewSet
class StudentReportViewSet(viewsets.ModelViewSet):
    serializer_class = StudentReportSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return StudentReport.objects.all()
        return StudentReport.objects.filter(student__class_instance__teacher__user=self.request.user)


# ClassPerformance ViewSet
class ClassPerformanceViewSet(viewsets.ModelViewSet):
    serializer_class = ClassPerformanceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return ClassPerformance.objects.all()
        return ClassPerformance.objects.filter(school_class__teacher__user=self.request.user)


# Subscription ViewSet
class SubscriptionViewSet(viewsets.ModelViewSet):
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Subscription.objects.all()
        return Subscription.objects.filter(teacher=self.request.user)


# PaymentRecord ViewSet
class PaymentRecordViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentRecordSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return PaymentRecord.objects.all()
        return PaymentRecord.objects.filter(teacher=self.request.user)