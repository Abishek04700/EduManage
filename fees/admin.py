from django.contrib import admin

from .models import FeePayment, FeeStructure


@admin.register(FeeStructure)
class FeeStructureAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'amount', 'due_date')
    list_filter = ('course',)


@admin.register(FeePayment)
class FeePaymentAdmin(admin.ModelAdmin):
    list_display = ('student', 'fee_structure', 'amount_paid', 'status', 'payment_date')
    list_filter = ('status', 'method')
    search_fields = ('student__admission_number', 'receipt_number')
