from datetime import date

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from academics.models import Course
from students.models import Student

from .models import Attendance


@login_required
def mark_attendance(request):
    if not (request.user.is_superuser or request.user.role in ('ADMIN', 'TEACHER')):
        messages.error(request, "You don't have permission to mark attendance.")
        return redirect('accounts:dashboard')

    courses = Course.objects.all()
    selected_course_id = request.GET.get('course') or request.POST.get('course')
    selected_date = request.GET.get('date') or request.POST.get('date') or date.today().isoformat()
    students = []

    if selected_course_id:
        students = Student.objects.filter(course_id=selected_course_id, status='ACTIVE').select_related('user')

    if request.method == 'POST' and selected_course_id:
        for student in students:
            status = request.POST.get(f'status_{student.id}', 'PRESENT')
            Attendance.objects.update_or_create(
                student=student, date=selected_date,
                defaults={'status': status, 'marked_by': request.user}
            )
        messages.success(request, 'Attendance saved successfully.')
        return redirect(f'/attendance/mark/?course={selected_course_id}&date={selected_date}')

    if selected_course_id:
        existing = {
            a.student_id: a.status for a in
            Attendance.objects.filter(student__course_id=selected_course_id, date=selected_date)
        }
        for s in students:
            s.current_status = existing.get(s.id, 'PRESENT')

    return render(request, 'attendance/mark_attendance.html', {
        'courses': courses,
        'students': students,
        'selected_course_id': int(selected_course_id) if selected_course_id else None,
        'selected_date': selected_date,
        'status_choices': Attendance.Status.choices,
    })


@login_required
def attendance_history(request):
    user = request.user
    if user.role == 'STUDENT':
        student = getattr(user, 'student_profile', None)
        records = Attendance.objects.filter(student=student) if student else Attendance.objects.none()
    else:
        records = Attendance.objects.select_related('student__user', 'student__course').all()
        course_id = request.GET.get('course')
        if course_id:
            records = records.filter(student__course_id=course_id)

    return render(request, 'attendance/attendance_history.html', {
        'records': records[:200],
        'courses': Course.objects.all(),
    })
