from django.db import models

from users.models import User

NULLABLE = {
    'null': True,
    'blank': True
}


class Course(models.Model):
    name = models.CharField(max_length=100, verbose_name='Name')
    preview = models.ImageField(**NULLABLE, upload_to='', verbose_name='Preview')
    description = models.TextField(**NULLABLE, verbose_name='Description')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Course'
        verbose_name_plural = 'Courses'


class Lesson(models.Model):
    name = models.CharField(max_length=50, verbose_name='Name')
    description = models.TextField(**NULLABLE, verbose_name='Description')
    preview = models.ImageField(**NULLABLE, upload_to='', verbose_name='Preview')
    video = models.URLField(**NULLABLE, max_length=300, verbose_name='Video')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Course')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Lesson'
        verbose_name_plural = 'Lessons'


class Payment(models.Model):
    payment_method = [
        ('cash', 'Cash'),
        ('card', 'Card')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='User')
    date_of_payment = models.DateField(auto_now_add=True, verbose_name='Date_of_payment')
    paid_course = models.ForeignKey(Course, on_delete=models.SET_NULL, **NULLABLE, verbose_name='Paid_course')
    paid_lesson = models.ForeignKey(Lesson, on_delete=models.SET_NULL, **NULLABLE, verbose_name='Paid_lesson')
    price = models.PositiveSmallIntegerField(verbose_name='Price')
    payment_method = models.CharField(choices=payment_method, verbose_name='Payment_method')

    def __str__(self):
        return f"{self.user.email} {'Course: ' + self.paid_course.name if self.paid_course else 'Lesson: ' + self.paid_lesson.name}"

    class Meta:
        verbose_name = 'Payment'
        verbose_name_plural = 'Payments'
        ordering = ('-date_of_payment',)
