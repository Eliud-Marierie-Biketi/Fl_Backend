from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    LoginView, TeacherViewSet, ProfileViewSet, ClassViewSet, SubjectViewSet,
    ExamViewSet, ExamSubjectViewSet, StudentViewSet, ScoreViewSet,
    ResultViewSet, StudentReportViewSet, ClassPerformanceViewSet,
    SubscriptionViewSet, PaymentRecordViewSet, UserRegistrationView
)

router = DefaultRouter()
router.register(r'teachers', TeacherViewSet)
router.register(r'profiles', ProfileViewSet)
router.register(r'classes', ClassViewSet)
router.register(r'subjects', SubjectViewSet)
router.register(r'exams', ExamViewSet)
router.register(r'exam-subjects', ExamSubjectViewSet)
router.register(r'students', StudentViewSet)
router.register(r'scores', ScoreViewSet)
router.register(r'results', ResultViewSet)
router.register(r'student-reports', StudentReportViewSet)
router.register(r'class-performance', ClassPerformanceViewSet)
router.register(r'subscriptions', SubscriptionViewSet)
router.register(r'payment-records', PaymentRecordViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('register/', UserRegistrationView.as_view(), name='user-register'),
    path('login/', LoginView.as_view(), name='user-login'),

]
