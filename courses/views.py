from django.http import HttpRequest
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from courses.models import Course, Lesson, Payment, Subscription
from courses.paginators import CoursesPaginator
from courses.permissions import IsModerator, IsOwner
from courses.serializers import CourseSerializer, LessonSerializer, PaymentSerializer, SubscriptionSerializer
from courses.services import get_payment_link
from courses.tasks import get_update_notification

# Create your views here.
class CourseViewSet(viewsets.ModelViewSet):
    """
       Manage courses, including creation, listing, and updates.

       This viewset allows you to perform various operations related to courses,
       such as creating new courses, listing available courses, and updating course details.
    """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = CoursesPaginator

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        instance = self.get_object()
        print(instance.id)
        get_update_notification.delay(instance.id)
        return response

    def get_queryset(self):
        queryset = super().get_queryset()

        if self.request.user.groups.filter(name='moderator').exists():
            return queryset.all()
        elif self.request.user:
            return queryset.filter(owner=self.request.user)
        else:
            return queryset.none()

    def perform_create(self, serializer):
        obj = serializer.save()
        obj.owner = self.request.user
        obj.save()


class LessonCreateAPIView(generics.CreateAPIView):
    """
        This view allows authenticated users to create new lessons within a course.
     """
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, ~IsModerator]

    def perform_create(self, serializer):
        new_moto = serializer.save()
        new_moto.owner = self.request.user
        new_moto.save()


class LessonListAPIView(generics.ListAPIView):
    """
      This view allows authenticated users to see all available lessons.
    """
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = CoursesPaginator

    def get_queryset(self):
        """
            Getting Lesson Objects based on User
        """
        queryset = super().get_queryset()

        if self.request.user.groups.filter(name='moderator').exists():
            return queryset.all()
        elif self.request.user:
            return queryset.filter(owner=self.request.user)
        else:
            return queryset.none()


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    """
        This view allows users to see details of a specific lesson.
        Access have only moderator and lesson's owner.
    """
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsOwner | IsModerator]


class LessonUpdateAPIView(generics.UpdateAPIView):
    """
        This view allows moderator and lesson's owner to update lesson details.
    """
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsOwner | IsModerator]


class LessonDestroyAPIView(generics.DestroyAPIView):
    """
        This view allows lesson's owner to delete a lesson.
    """
    queryset = Lesson.objects.all()
    permission_classes = [IsOwner]


class PaymentListAPIView(ListAPIView):
    """
        Retrieve a list of payments.

        This view allows users to see a list of payments. It supports ordering and filtering by course and payment method.
        - Admin users can view all payments.
        - Authenticated users can view their own payments.
    """
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('lesson', 'course', 'payment_method')
    ordering_fields = ('date_of_payment',)

    def get_queryset(self):
        queryset = super().get_queryset()

        return queryset.filter(user=self.request.user)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def subscribe_to_updates(request: HttpRequest, pk: int) -> Response:
    """
        Submission to subscribe to course updates or unsubscribe.
        Prohibited for unauthorized users
    """

    try:
        course = Course.objects.get(pk=pk)
    except Course.DoesNotExist:
        return Response({"error": "This course doesn't exist."}, status=status.HTTP_400_BAD_REQUEST)
    else:
        if Subscription.objects.filter(course=course, user=request.user).exists():
            Subscription.objects.filter(course=course, user=request.user).delete()
            return Response({'message': f'Subscribe for course updates {course.name} has been cancelled!'},
                            status=status.HTTP_200_OK)

        data = {'course': pk, 'user': request.user.id}
        serializer = SubscriptionSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': f'Subscribe for course - {course.name}, updates !'},
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def payment_for_course(request, pk):
    """
       Create a new payment session for the specified course.

       This view allows authenticated users to create a new payment session for a specific course. It generates
       a payment session with a Stripe link and returns payment link.
    """
    try:
        payment_link = get_payment_link(pk)
    except Course.DoesNotExist:
        return Response({"error": "This course doesn't exist."}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'payment_link': payment_link})
