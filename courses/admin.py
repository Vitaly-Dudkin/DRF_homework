from django.contrib import admin

from courses.models import Payment


# Register your models here.
@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'date_of_payment', 'price', 'payment_method',)
