from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import DeleteView, ListView

from accounts.mixins import AdminRequiredMixin

from .forms import CourseForm, SubjectForm
from .models import Course, Subject


class CourseListView(LoginRequiredMixin, ListView):
    model = Course
    template_name = 'academics/course_list.html'
    context_object_name = 'courses'

    def get_queryset(self):
        return Course.objects.select_related('academic_year', 'class_teacher').prefetch_related('subjects')


class CourseDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = Course
    template_name = 'academics/course_confirm_delete.html'
    success_url = '/academics/courses/'


def course_form_view(request, pk=None):
    if not (request.user.is_authenticated and (request.user.is_superuser or request.user.role == 'ADMIN')):
        messages.error(request, "You don't have permission to manage courses.")
        return redirect('accounts:dashboard')

    course = get_object_or_404(Course, pk=pk) if pk else None
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, 'Course saved successfully.')
            return redirect('academics:course_list')
    else:
        form = CourseForm(instance=course)
    return render(request, 'academics/course_form.html', {'form': form, 'course': course})


class SubjectListView(LoginRequiredMixin, ListView):
    model = Subject
    template_name = 'academics/subject_list.html'
    context_object_name = 'subjects'

    def get_queryset(self):
        return Subject.objects.select_related('course', 'teacher')


class SubjectDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = Subject
    template_name = 'academics/subject_confirm_delete.html'
    success_url = '/academics/subjects/'


def subject_form_view(request, pk=None):
    if not (request.user.is_authenticated and (request.user.is_superuser or request.user.role == 'ADMIN')):
        messages.error(request, "You don't have permission to manage subjects.")
        return redirect('accounts:dashboard')

    subject = get_object_or_404(Subject, pk=pk) if pk else None
    if request.method == 'POST':
        form = SubjectForm(request.POST, instance=subject)
        if form.is_valid():
            form.save()
            messages.success(request, 'Subject saved successfully.')
            return redirect('academics:subject_list')
    else:
        form = SubjectForm(instance=subject)
    return render(request, 'academics/subject_form.html', {'form': form, 'subject': subject})
