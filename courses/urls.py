from django.urls import path
from rest_framework import routers

from courses.apps import CoursesConfig
from courses.views import CourseViewSet, LessonCreateAPIView, LessonListAPIView, LessonRetrieveAPIView, \
    LessonUpdateAPIView, LessonDestroyAPIView, PaymentListAPIView, subscribe_to_updates

router = routers.DefaultRouter()
router.register(r'courses', CourseViewSet)

app_name = CoursesConfig.name

urlpatterns = [
    path('lesson_create/', LessonCreateAPIView.as_view(), name='create'),
    path('lesson_list/', LessonListAPIView.as_view(), name='list'),
    path('lessonn_detail/<int:pk>/', LessonRetrieveAPIView.as_view(), name='detail'),
    path('lesson_update/<int:pk>/', LessonUpdateAPIView.as_view(), name='update'),
    path('lesson_delete/<int:pk>/', LessonDestroyAPIView.as_view(), name='delete'),

    path('payment/<int:pk>/', PaymentListAPIView.as_view(), name='payment'),  # how does it work?
    path('subscribe/<int:pk>/', subscribe_to_updates, name='subscribe_to_updates')

] + router.urls

