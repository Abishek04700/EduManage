from datetime import date, timedelta

from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout as auth_logout
from django.shortcuts import redirect, render

from academics.models import Course
from attendance.models import Attendance
from exams.models import Result
from fees.models import FeePayment
from notices.models import Notice
from students.models import Student
from teachers.models import Teacher

from .forms import LoginForm
from .models import User


class SMSLoginView(LoginView):
    template_name = 'accounts/login.html'
    authentication_form = LoginForm
    redirect_authenticated_user = True


def logout_view(request):
    auth_logout(request)
    return redirect('accounts:login')


@login_required
def dashboard(request):
    user = request.user
    context = {'user': user}

    notices = Notice.objects.filter(audience='ALL')
    if user.role == 'TEACHER':
        notices = notices | Notice.objects.filter(audience='TEACHERS')
    if user.role == 'STUDENT':
        notices = notices | Notice.objects.filter(audience='STUDENTS')
    context['notices'] = notices.distinct()[:5]

    if user.is_superuser or user.role == User.Role.ADMIN:
        today = date.today()
        week_ago = today - timedelta(days=6)
        context.update({
            'total_students': Student.objects.filter(status='ACTIVE').count(),
            'total_teachers': Teacher.objects.count(),
            'total_courses': Course.objects.count(),
            'fees_pending': FeePayment.objects.filter(status='PENDING').count(),
            'fees_collected': sum(
                p.amount_paid for p in FeePayment.objects.filter(status='PAID')
            ),
            'attendance_today': Attendance.objects.filter(date=today).count(),
            'recent_attendance': Attendance.objects.select_related('student__user').order_by('-date')[:8],
            'weekly_attendance_labels': [
                (week_ago + timedelta(days=i)).strftime('%a') for i in range(7)
            ],
            'weekly_attendance_present': [
                Attendance.objects.filter(date=week_ago + timedelta(days=i), status='PRESENT').count()
                for i in range(7)
            ],
            'weekly_attendance_absent': [
                Attendance.objects.filter(date=week_ago + timedelta(days=i), status='ABSENT').count()
                for i in range(7)
            ],
        })
        return render(request, 'accounts/dashboard_admin.html', context)

    if user.role == User.Role.TEACHER:
        teacher = Teacher.objects.filter(user=user).first()
        context['teacher'] = teacher
        if teacher:
            context['my_subjects'] = teacher.subjects.all()
            context['my_classes'] = teacher.classes_led.all()
        return render(request, 'accounts/dashboard_teacher.html', context)

    if user.role == User.Role.STUDENT:
        student = Student.objects.filter(user=user).first()
        context['student'] = student
        if student:
            context['recent_results'] = Result.objects.filter(student=student).select_related(
                'exam', 'subject'
            ).order_by('-exam__start_date')[:5]
            context['attendance_summary'] = {
                'present': Attendance.objects.filter(student=student, status='PRESENT').count(),
                'absent': Attendance.objects.filter(student=student, status='ABSENT').count(),
                'late': Attendance.objects.filter(student=student, status='LATE').count(),
            }
            context['fee_payments'] = FeePayment.objects.filter(student=student).select_related(
                'fee_structure'
            )[:5]
        return render(request, 'accounts/dashboard_student.html', context)

    return render(request, 'accounts/dashboard_admin.html', context)
