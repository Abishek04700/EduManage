from django.db import models


class FeeStructure(models.Model):
    course = models.ForeignKey('academics.Course', on_delete=models.CASCADE, related_name='fee_structures')
    title = models.CharField(max_length=100, help_text="e.g. Tuition Fee, Term 1")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()

    class Meta:
        ordering = ['due_date']

    def __str__(self):
        return f"{self.title} - {self.course} - {self.amount}"


class FeePayment(models.Model):
    class PaymentStatus(models.TextChoices):
        PAID = 'PAID', 'Paid'
        PENDING = 'PENDING', 'Pending'
        OVERDUE = 'OVERDUE', 'Overdue'

    class Method(models.TextChoices):
        CASH = 'CASH', 'Cash'
        CARD = 'CARD', 'Card'
        BANK_TRANSFER = 'BANK_TRANSFER', 'Bank Transfer'
        ONLINE = 'ONLINE', 'Online'

    student = models.ForeignKey('students.Student', on_delete=models.CASCADE, related_name='fee_payments')
    fee_structure = models.ForeignKey(FeeStructure, on_delete=models.CASCADE, related_name='payments')
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    payment_date = models.DateField(blank=True, null=True)
    method = models.CharField(max_length=20, choices=Method.choices, default=Method.CASH)
    status = models.CharField(max_length=10, choices=PaymentStatus.choices, default=PaymentStatus.PENDING)
    receipt_number = models.CharField(max_length=30, blank=True, unique=True, null=True)

    class Meta:
        ordering = ['-payment_date']

    def __str__(self):
        return f"{self.student} - {self.fee_structure} - {self.get_status_display()}"
