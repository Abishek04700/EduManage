from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import DeleteView, DetailView, ListView

from accounts.mixins import StaffRequiredMixin
from students.models import Student

from .forms import ExamForm, ResultForm
from .models import Exam, Result


class ExamListView(LoginRequiredMixin, ListView):
    model = Exam
    template_name = 'exams/exam_list.html'
    context_object_name = 'exams'

    def get_queryset(self):
        return Exam.objects.select_related('course')


class ExamDetailView(LoginRequiredMixin, DetailView):
    model = Exam
    template_name = 'exams/exam_detail.html'
    context_object_name = 'exam'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['results'] = self.object.results.select_related('student__user', 'subject')
        return ctx


class ExamDeleteView(LoginRequiredMixin, StaffRequiredMixin, DeleteView):
    model = Exam
    template_name = 'exams/exam_confirm_delete.html'
    success_url = '/exams/'


@login_required
def exam_form_view(request, pk=None):
    if not (request.user.is_superuser or request.user.role in ('ADMIN', 'TEACHER')):
        messages.error(request, "You don't have permission to manage exams.")
        return redirect('accounts:dashboard')

    exam = get_object_or_404(Exam, pk=pk) if pk else None
    if request.method == 'POST':
        form = ExamForm(request.POST, instance=exam)
        if form.is_valid():
            form.save()
            messages.success(request, 'Exam saved successfully.')
            return redirect('exams:list')
    else:
        form = ExamForm(instance=exam)
    return render(request, 'exams/exam_form.html', {'form': form, 'exam': exam})


@login_required
def result_entry(request, exam_id):
    exam = get_object_or_404(Exam, pk=exam_id)
    if not (request.user.is_superuser or request.user.role in ('ADMIN', 'TEACHER')):
        messages.error(request, "You don't have permission to enter results.")
        return redirect('accounts:dashboard')

    if request.method == 'POST':
        form = ResultForm(request.POST)
        if form.is_valid():
            result = form.save(commit=False)
            result.exam = exam
            result.save()
            messages.success(request, 'Result added successfully.')
            return redirect('exams:detail', pk=exam.pk)
    else:
        form = ResultForm()
        form.fields['student'].queryset = Student.objects.filter(course=exam.course)
        form.fields['subject'].queryset = exam.course.subjects.all()

    return render(request, 'exams/result_form.html', {'form': form, 'exam': exam})
