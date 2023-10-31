from django.contrib import admin

from courses.models import Payment, Course, Lesson


# Register your models here.
@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'date_of_payment', 'price', 'payment_method',)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'owner')


@admin.register(Lesson)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'owner')
