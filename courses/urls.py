from django.urls import path
from rest_framework import routers

from courses.apps import CoursesConfig
from courses.views import CourseViewSet, LessonCreateAPIView, LessonListAPIView, LessonRetrieveAPIView, \
    LessonUpdateAPIView, LessonDestroyAPIView

router = routers.DefaultRouter()
router.register(r'courses', CourseViewSet)

app_name = CoursesConfig.name

urlpatterns = [
    path('create/', LessonCreateAPIView.as_view(), name='create'),
    path('list/',LessonListAPIView.as_view(), name='list'),
    path('retrieve/<int:pk>/', LessonRetrieveAPIView.as_view(), name='retrieve'),
    path('update/<int:pk>/', LessonUpdateAPIView.as_view(), name='update'),
    path('destroy/<int:pk>/', LessonDestroyAPIView.as_view(), name='destroy'),
] + router.urls

