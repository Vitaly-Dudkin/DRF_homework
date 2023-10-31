from rest_framework import serializers

from courses.models import Course, Lesson, Payment, Subscription
from courses.validators import validate_url


class LessonSerializer(serializers.ModelSerializer):
    video = serializers.URLField(validators=[validate_url], required=False)

    class Meta:
        model = Lesson
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    lesson_count = serializers.SerializerMethodField(read_only=True)
    lesson = LessonSerializer(source='lesson_set', read_only=True, many=True)
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    def get_lesson_count(self, instance):
        return instance.lesson_set.count()

    def get_is_subscribed(self, course):
        user = self.context['request'].user
        return course.subscription_set.filter(user=user).exists()

    class Meta:
        model = Course
        fields = ("id", 'name', 'preview', 'description', 'lesson', 'lesson_count', 'is_subscribed')


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'


class SubscriptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subscription
        fields = ('course', 'user')
