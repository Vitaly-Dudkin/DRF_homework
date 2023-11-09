from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail

from courses.models import Subscription, Course


@shared_task
def get_update_notification(course):
    subscribes = Subscription.objects.filter(course=course)
    print(subscribes)
    if subscribes:
        for sub in subscribes:
            print(sub.user.email)
            print(sub.course.name)
            send_mail(
                subject=f'update news abot course - {sub.course.name}',
                message=f"Some updates about course",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[sub.user.email]
            )
