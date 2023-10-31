from datetime import datetime, timedelta

from celery import shared_task

from users.models import User


@shared_task
def check_is_active():
    three_months = datetime.now() - timedelta(days=90)
    User.objects.filter(last_login__lt=three_months).update(is_active=False)