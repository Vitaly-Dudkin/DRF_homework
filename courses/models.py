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
    price = models.PositiveIntegerField(default=32000, verbose_name='Price')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Owner', **NULLABLE)

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
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Owner', **NULLABLE)

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
    paid_course = models.ForeignKey(Course, on_delete=models.SET_NULL, **NULLABLE, verbose_name='Paid_course')

    date_of_payment = models.DateField(auto_now_add=True, verbose_name='Date_of_payment')

    price = models.PositiveSmallIntegerField(verbose_name='Price')
    payment_method = models.CharField(choices=payment_method, verbose_name='Payment_method')

    def __str__(self):
        return f"{self.date_of_payment}: {self.user} - {self.price}"

    class Meta:
        verbose_name = 'Payment'
        verbose_name_plural = 'Payments'
        ordering = ('-date_of_payment',)


class Subscription(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='course')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='course')

    def __str__(self):
        return f'{self.user.email} - {self.course.name}'

    class Meta:
        verbose_name = 'Subscription'
        verbose_name_plural = 'Subscriptions'
