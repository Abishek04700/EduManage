
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import DeleteView, DetailView, ListView

from accounts.mixins import StaffRequiredMixin
from .forms import StudentProfileForm, StudentUserForm
from .models import Student


def is_staff_user(user):
    return (
        user.is_authenticated
        and (
            user.is_superuser
            or user.role in ('ADMIN', 'TEACHER')
        )
    )


class StudentListView(
    LoginRequiredMixin, StaffRequiredMixin, ListView
):
    model = Student
    template_name = 'students/student_list.html'
    context_object_name = 'students'
    paginate_by = 15

    def get_queryset(self):
        qs = Student.objects.select_related(
            'user', 'course'
        ).all()

        q = self.request.GET.get('q')
        if q:
            qs = qs.filter(
                Q(user__first_name__icontains=q)
                | Q(user__last_name__icontains=q)
                | Q(admission_number__icontains=q)
                | Q(roll_number__icontains=q)
            )

        course = self.request.GET.get('course')
        if course:
            qs = qs.filter(course_id=course)

        return qs

    def get_context_data(self, **kwargs):
        from academics.models import Course

        ctx = super().get_context_data(**kwargs)
        ctx['courses'] = Course.objects.all()
        ctx['query'] = self.request.GET.get('q', '')
        return ctx


class StudentDetailView(LoginRequiredMixin, DetailView):
    model = Student
    template_name = 'students/student_detail.html'
    context_object_name = 'student'

    def get_queryset(self):
        qs = Student.objects.select_related('user', 'course')
        user = self.request.user

        if is_staff_user(user):
            return qs

        # Students can view only their own details.
        return qs.filter(user=user)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        student = self.object

        ctx['results'] = student.results.select_related(
            'exam', 'subject'
        )
        ctx['attendance'] = student.attendance_records.all()[:20]
        ctx['fee_payments'] = student.fee_payments.select_related(
            'fee_structure'
        )

        return ctx


class StudentDeleteView(
    LoginRequiredMixin, StaffRequiredMixin, DeleteView
):
    model = Student
    template_name = 'students/student_confirm_delete.html'
    success_url = '/students/'

    def form_valid(self, form):
        messages.success(
            self.request,
            'Student removed successfully.'
        )
        return super().form_valid(form)


@login_required
def student_create(request):
    if not is_staff_user(request.user):
        messages.error(
            request,
            "You don't have permission to add students."
        )
        return redirect('accounts:dashboard')

    if request.method == 'POST':
        user_form = StudentUserForm(
            request.POST, request.FILES
        )
        profile_form = StudentProfileForm(
            request.POST, is_staff_user=True
        )

        if user_form.is_valid() and profile_form.is_valid():
            with transaction.atomic():
                user = user_form.save()
                student = profile_form.save(commit=False)
                student.user = user
                student.save()

            messages.success(
                request,
                f'Student {user.get_full_name()} added successfully.'
            )
            return redirect('students:list')

    else:
        user_form = StudentUserForm()
        profile_form = StudentProfileForm(is_staff_user=True)

    return render(
        request,
        'students/student_form.html',
        {
            'user_form': user_form,
            'profile_form': profile_form,
            'title': 'Add Student',
        }
    )


@login_required
def student_update(request, pk):
    student = get_object_or_404(Student, pk=pk)

    staff_user = is_staff_user(request.user)
    own_profile = request.user == student.user

    if not (staff_user or own_profile):
        messages.error(
            request,
            "You don't have permission to edit this student."
        )
        return redirect('accounts:dashboard')

    if request.method == 'POST':
        user_form = StudentUserForm(
            request.POST,
            request.FILES,
            instance=student.user,
        )
        profile_form = StudentProfileForm(
            request.POST,
            instance=student,
            is_staff_user=staff_user,
        )

        if user_form.is_valid() and profile_form.is_valid():
            with transaction.atomic():
                user_form.save()
                profile_form.save()

            messages.success(
                request,
                'Student updated successfully.'
            )
            return redirect(
                'students:detail',
                pk=student.pk,
            )

    else:
        user_form = StudentUserForm(instance=student.user)
        profile_form = StudentProfileForm(
            instance=student,
            is_staff_user=staff_user,
        )

    return render(
        request,
        'students/student_form.html',
        {
            'user_form': user_form,
            'profile_form': profile_form,
            'title': 'Edit Student',
            'student': student,
        }
    )
