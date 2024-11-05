from rest_framework import viewsets, generics
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


class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(username=serializer.validated_data['username'], 
                            password=serializer.validated_data['password'])
        # Create or retrieve the token for the user
        token, created = Token.objects.get_or_create(user=user)

        return Response({
            'token': token.key,
            'user_id': user.id,
            'username': user.username
        }, status=status.HTTP_200_OK)    
    
    
# Teacher ViewSet
class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    permission_classes = [IsAuthenticated]

# Profile ViewSet
class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

# Class ViewSet
class ClassViewSet(viewsets.ModelViewSet):
    queryset = Class.objects.all()
    serializer_class = ClassSerializer
    permission_classes = [IsAuthenticated]

# Subject ViewSet
class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = [IsAuthenticated]

# Exam ViewSet
class ExamViewSet(viewsets.ModelViewSet):
    queryset = Exam.objects.all()
    serializer_class = ExamSerializer
    permission_classes = [IsAuthenticated]

# ExamSubject ViewSet
class ExamSubjectViewSet(viewsets.ModelViewSet):
    queryset = ExamSubject.objects.all()
    serializer_class = ExamSubjectSerializer
    permission_classes = [IsAuthenticated]

# Student ViewSet
class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]

# Score ViewSet
class ScoreViewSet(viewsets.ModelViewSet):
    queryset = Score.objects.all()
    serializer_class = ScoreSerializer
    permission_classes = [IsAuthenticated]

# Result ViewSet
class ResultViewSet(viewsets.ModelViewSet):
    queryset = Result.objects.all()
    serializer_class = ResultSerializer
    permission_classes = [IsAuthenticated]

# StudentReport ViewSet
class StudentReportViewSet(viewsets.ModelViewSet):
    queryset = StudentReport.objects.all()
    serializer_class = StudentReportSerializer
    permission_classes = [IsAuthenticated]

# ClassPerformance ViewSet
class ClassPerformanceViewSet(viewsets.ModelViewSet):
    queryset = ClassPerformance.objects.all()
    serializer_class = ClassPerformanceSerializer
    permission_classes = [IsAuthenticated]

# Subscription ViewSet
class SubscriptionViewSet(viewsets.ModelViewSet):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]

# PaymentRecord ViewSet
class PaymentRecordViewSet(viewsets.ModelViewSet):
    queryset = PaymentRecord.objects.all()
    serializer_class = PaymentRecordSerializer
    permission_classes = [IsAuthenticated]
