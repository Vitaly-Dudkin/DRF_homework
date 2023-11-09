from datetime import datetime, timedelta

from celery import shared_task

from users.models import User


@shared_task
def check_is_active():
    one_months = datetime.now() - timedelta(days=32)
    User.objects.filter(last_login__lt=one_months).update(is_active=False)