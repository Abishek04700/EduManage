from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import DeleteView, ListView

from accounts.mixins import StaffRequiredMixin

from .forms import NoticeForm
from .models import Notice


class NoticeListView(LoginRequiredMixin, ListView):
    model = Notice
    template_name = 'notices/notice_list.html'
    context_object_name = 'notices'
    paginate_by = 10

    def get_queryset(self):
        user = self.request.user
        qs = Notice.objects.filter(audience='ALL')
        if user.role == 'TEACHER':
            qs = qs | Notice.objects.filter(audience='TEACHERS')
        if user.role == 'STUDENT':
            qs = qs | Notice.objects.filter(audience='STUDENTS')
        if user.is_superuser or user.role == 'ADMIN':
            qs = Notice.objects.all()
        return qs.distinct()


@login_required
def notice_form_view(request, pk=None):
    if not (request.user.is_superuser or request.user.role in ('ADMIN', 'TEACHER')):
        messages.error(request, "You don't have permission to post notices.")
        return redirect('accounts:dashboard')

    notice = get_object_or_404(Notice, pk=pk) if pk else None
    if request.method == 'POST':
        form = NoticeForm(request.POST, instance=notice)
        if form.is_valid():
            obj = form.save(commit=False)
            if not obj.posted_by_id:
                obj.posted_by = request.user
            obj.save()
            messages.success(request, 'Notice posted successfully.')
            return redirect('notices:list')
    else:
        form = NoticeForm(instance=notice)
    return render(request, 'notices/notice_form.html', {'form': form, 'notice': notice})


class NoticeDeleteView(LoginRequiredMixin, StaffRequiredMixin, DeleteView):
    model = Notice
    template_name = 'notices/notice_confirm_delete.html'
    success_url = '/notices/'
