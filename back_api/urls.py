from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    LoginView, TeacherViewSet, ProfileViewSet, ClassViewSet, SubjectViewSet,
    ExamViewSet, ExamSubjectViewSet, StudentViewSet, ScoreViewSet,
    ResultViewSet, StudentReportViewSet, ClassPerformanceViewSet,
    SubscriptionViewSet, PaymentRecordViewSet, UserRegistrationView
)

router = DefaultRouter()
router.register(r'teachers', TeacherViewSet, basename='teacher')
router.register(r'profiles', ProfileViewSet, basename='profile')
router.register(r'classes', ClassViewSet, basename='class')
router.register(r'subjects', SubjectViewSet, basename='subject')
router.register(r'exams', ExamViewSet, basename='exam')
router.register(r'exam-subjects', ExamSubjectViewSet, basename='exam-subject')
router.register(r'students', StudentViewSet, basename='student')
router.register(r'scores', ScoreViewSet, basename='score')
router.register(r'results', ResultViewSet, basename='result')
router.register(r'student-reports', StudentReportViewSet, basename='student-report')
router.register(r'class-performance', ClassPerformanceViewSet, basename='class-performance')
router.register(r'subscriptions', SubscriptionViewSet, basename='subscription')
router.register(r'payment-records', PaymentRecordViewSet, basename='payment-record')

urlpatterns = [
    path('', include(router.urls)),
    path('register/', UserRegistrationView.as_view(), name='user-register'),
    path('login/', LoginView.as_view(), name='user-login'),

]
