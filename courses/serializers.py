from rest_framework import serializers

from courses.models import Course, Lesson, Payment
from courses.validators import validate_url


class LessonSerializer(serializers.ModelSerializer):
    video = serializers.URLField(validators=[validate_url])

    class Meta:
        model = Lesson
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    lesson_count = serializers.SerializerMethodField()
    lesson = LessonSerializer(source='lesson_set', read_only=True, many=True)

    def get_lesson_count(self, instance):
        return instance.lesson_set.count()

    class Meta:
        model = Course
        fields = ('name', 'preview', 'description', 'lesson', 'lesson_count')


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'
