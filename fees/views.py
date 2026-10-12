from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import DeleteView, ListView

from accounts.mixins import AdminRequiredMixin

from .forms import FeePaymentForm, FeeStructureForm
from .models import FeePayment, FeeStructure


class FeeStructureListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = FeeStructure
    template_name = 'fees/structure_list.html'
    context_object_name = 'structures'

    def get_queryset(self):
        return FeeStructure.objects.select_related('course')


@login_required
def fee_structure_form_view(request, pk=None):
    if not (request.user.is_superuser or request.user.role == 'ADMIN'):
        messages.error(request, "You don't have permission to manage fee structures.")
        return redirect('accounts:dashboard')

    structure = get_object_or_404(FeeStructure, pk=pk) if pk else None
    if request.method == 'POST':
        form = FeeStructureForm(request.POST, instance=structure)
        if form.is_valid():
            form.save()
            messages.success(request, 'Fee structure saved.')
            return redirect('fees:structure_list')
    else:
        form = FeeStructureForm(instance=structure)
    return render(request, 'fees/structure_form.html', {'form': form, 'structure': structure})


class FeeStructureDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = FeeStructure
    template_name = 'fees/structure_confirm_delete.html'
    success_url = '/fees/structures/'


class FeePaymentListView(LoginRequiredMixin, ListView):
    model = FeePayment
    template_name = 'fees/payment_list.html'
    context_object_name = 'payments'
    paginate_by = 20

    def get_queryset(self):
        user = self.request.user
        qs = FeePayment.objects.select_related('student__user', 'fee_structure')
        if user.role == 'STUDENT':
            qs = qs.filter(student__user=user)
        status = self.request.GET.get('status')
        if status:
            qs = qs.filter(status=status)
        return qs


@login_required
def fee_payment_form_view(request, pk=None):
    if not (request.user.is_superuser or request.user.role == 'ADMIN'):
        messages.error(request, "You don't have permission to manage fee payments.")
        return redirect('accounts:dashboard')

    payment = get_object_or_404(FeePayment, pk=pk) if pk else None
    if request.method == 'POST':
        form = FeePaymentForm(request.POST, instance=payment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Fee payment saved.')
            return redirect('fees:payment_list')
    else:
        form = FeePaymentForm(instance=payment)
    return render(request, 'fees/payment_form.html', {'form': form, 'payment': payment})


class FeePaymentDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = FeePayment
    template_name = 'fees/payment_confirm_delete.html'
    success_url = '/fees/payments/'
