from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import DeleteView, DetailView, ListView

from accounts.mixins import AdminRequiredMixin

from .forms import TeacherProfileForm, TeacherUserForm
from .models import Teacher


class TeacherListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = Teacher
    template_name = 'teachers/teacher_list.html'
    context_object_name = 'teachers'
    paginate_by = 15

    def get_queryset(self):
        qs = Teacher.objects.select_related('user').all()
        q = self.request.GET.get('q')
        if q:
            qs = qs.filter(
                Q(user__first_name__icontains=q) |
                Q(user__last_name__icontains=q) |
                Q(employee_id__icontains=q)
            )
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['query'] = self.request.GET.get('q', '')
        return ctx


class TeacherDetailView(LoginRequiredMixin, DetailView):
    model = Teacher
    template_name = 'teachers/teacher_detail.html'
    context_object_name = 'teacher'


class TeacherDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = Teacher
    template_name = 'teachers/teacher_confirm_delete.html'
    success_url = '/teachers/'

    def form_valid(self, form):
        messages.success(self.request, 'Teacher removed successfully.')
        return super().form_valid(form)


@login_required
def teacher_create(request):
    if not (request.user.is_superuser or request.user.role == 'ADMIN'):
        messages.error(request, "You don't have permission to add teachers.")
        return redirect('accounts:dashboard')

    if request.method == 'POST':
        user_form = TeacherUserForm(request.POST, request.FILES)
        profile_form = TeacherProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            with transaction.atomic():
                user = user_form.save()
                teacher = profile_form.save(commit=False)
                teacher.user = user
                teacher.save()
            messages.success(request, f'Teacher {user.get_full_name()} added successfully.')
            return redirect('teachers:list')
    else:
        user_form = TeacherUserForm()
        profile_form = TeacherProfileForm()

    return render(request, 'teachers/teacher_form.html', {
        'user_form': user_form, 'profile_form': profile_form, 'title': 'Add Teacher'
    })


@login_required
def teacher_update(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)
    if not (request.user.is_superuser or request.user.role == 'ADMIN' or request.user == teacher.user):
        messages.error(request, "You don't have permission to edit this teacher.")
        return redirect('accounts:dashboard')

    if request.method == 'POST':
        user_form = TeacherUserForm(request.POST, request.FILES, instance=teacher.user)
        profile_form = TeacherProfileForm(request.POST, instance=teacher)
        if user_form.is_valid() and profile_form.is_valid():
            with transaction.atomic():
                user_form.save()
                profile_form.save()
            messages.success(request, 'Teacher updated successfully.')
            return redirect('teachers:detail', pk=teacher.pk)
    else:
        user_form = TeacherUserForm(instance=teacher.user)
        profile_form = TeacherProfileForm(instance=teacher)

    return render(request, 'teachers/teacher_form.html', {
        'user_form': user_form, 'profile_form': profile_form, 'title': 'Edit Teacher', 'teacher': teacher
    })
