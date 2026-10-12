from django import forms

from .models import FeePayment, FeeStructure


class FeeStructureForm(forms.ModelForm):
    class Meta:
        model = FeeStructure
        fields = ['course', 'title', 'amount', 'due_date']
        widgets = {'due_date': forms.DateInput(attrs={'type': 'date'})}


class FeePaymentForm(forms.ModelForm):
    class Meta:
        model = FeePayment
        fields = ['student', 'fee_structure', 'amount_paid', 'payment_date', 'method', 'status', 'receipt_number']
        widgets = {'payment_date': forms.DateInput(attrs={'type': 'date'})}
