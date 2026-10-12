import random
from datetime import date, timedelta

from django.core.management.base import BaseCommand
from django.db import transaction

from academics.models import AcademicYear, Course, Subject
from accounts.models import User
from attendance.models import Attendance
from exams.models import Exam, Result
from fees.models import FeePayment, FeeStructure
from notices.models import Notice
from students.models import Student
from teachers.models import Teacher


class Command(BaseCommand):
    help = "Seed the database with demo accounts and sample data."

    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write("Seeding demo data...")

        # --- Superuser / Admin ---
        if not User.objects.filter(username="admin").exists():
            admin = User.objects.create_superuser(
                username="admin", email="admin@edumanage.test", password="admin123",
                first_name="System", last_name="Admin", role=User.Role.ADMIN,
            )
        else:
            admin = User.objects.get(username="admin")
        self.stdout.write(self.style.SUCCESS("  Admin: admin / admin123"))

        # --- Academic year & courses ---
        year, _ = AcademicYear.objects.get_or_create(name="2025-2026", defaults={"is_current": True})

        course_names = [("Grade 9", "A"), ("Grade 10", "A"), ("Grade 11", "A")]
        courses = []
        for name, section in course_names:
            c, _ = Course.objects.get_or_create(name=name, section=section, academic_year=year)
            courses.append(c)

        # --- Teachers ---
        teacher_data = [
            ("teacher1", "Alice", "Morgan", "Mathematics", "M.Sc. Mathematics"),
            ("teacher2", "Brian", "Lee", "Science", "M.Sc. Physics"),
            ("teacher3", "Carla", "Nunez", "English", "M.A. English Literature"),
        ]
        teachers = []
        for i, (uname, first, last, subj, qual) in enumerate(teacher_data, start=1):
            if not User.objects.filter(username=uname).exists():
                u = User.objects.create_user(
                    username=uname, email=f"{uname}@edumanage.test", password="teacher123",
                    first_name=first, last_name=last, role=User.Role.TEACHER,
                )
            else:
                u = User.objects.get(username=uname)
            t, _ = Teacher.objects.get_or_create(
                user=u, defaults={
                    "employee_id": f"EMP00{i}", "qualification": qual,
                    "specialization": subj, "joining_date": date(2022, 6, 1),
                    "salary": 45000 + i * 2000,
                }
            )
            teachers.append(t)
        self.stdout.write(self.style.SUCCESS("  Teachers: teacher1 / teacher2 / teacher3 (password: teacher123)"))

        # Assign class teachers
        for course, teacher in zip(courses, teachers):
            course.class_teacher = teacher
            course.save()

        # --- Subjects ---
        subject_defs = [
            ("Mathematics", "MATH"), ("Science", "SCI"), ("English", "ENG"),
        ]
        for course in courses:
            for idx, (sname, scode) in enumerate(subject_defs):
                Subject.objects.get_or_create(
                    name=sname, code=f"{scode}-{course.name.split()[-1]}",
                    course=course, defaults={"teacher": teachers[idx % len(teachers)]}
                )

        # --- Students ---
        first_names = ["John", "Emma", "Liam", "Olivia", "Noah", "Ava", "Ethan", "Sophia"]
        last_names = ["Smith", "Johnson", "Brown", "Davis", "Miller", "Wilson", "Moore", "Taylor"]
        students = []
        student_count = 0
        for course in courses:
            for i in range(4):
                student_count += 1
                uname = f"student{student_count}"
                first = random.choice(first_names)
                last = random.choice(last_names)
                if not User.objects.filter(username=uname).exists():
                    u = User.objects.create_user(
                        username=uname, email=f"{uname}@edumanage.test", password="student123",
                        first_name=first, last_name=last, role=User.Role.STUDENT,
                    )
                else:
                    u = User.objects.get(username=uname)
                s, _ = Student.objects.get_or_create(
                    user=u, defaults={
                        "admission_number": f"ADM{1000 + student_count}",
                        "roll_number": str(i + 1),
                        "course": course,
                        "gender": random.choice(["M", "F"]),
                        "guardian_name": f"{last} Family",
                        "guardian_phone": "555-0100",
                        "status": Student.Status.ACTIVE,
                    }
                )
                students.append(s)
        self.stdout.write(self.style.SUCCESS("  Students: student1 ... student12 (password: student123)"))

        # --- Attendance (last 7 days) ---
        today = date.today()
        for i in range(7):
            d = today - timedelta(days=i)
            for s in students:
                Attendance.objects.update_or_create(
                    student=s, date=d,
                    defaults={
                        "status": random.choices(
                            ["PRESENT", "ABSENT", "LATE"], weights=[80, 10, 10]
                        )[0],
                        "marked_by": admin,
                    }
                )

        # --- Exam & Results ---
        for course in courses:
            exam, _ = Exam.objects.get_or_create(
                name="Mid Term", course=course,
                defaults={"start_date": today - timedelta(days=20), "end_date": today - timedelta(days=15)}
            )
            for s in Student.objects.filter(course=course):
                for subject in course.subjects.all():
                    Result.objects.get_or_create(
                        exam=exam, student=s, subject=subject,
                        defaults={"marks_obtained": random.randint(55, 98), "max_marks": 100}
                    )

        # --- Fees ---
        for course in courses:
            fs, _ = FeeStructure.objects.get_or_create(
                course=course, title="Term 1 Tuition",
                defaults={"amount": 1200, "due_date": today + timedelta(days=30)}
            )
            for s in Student.objects.filter(course=course):
                FeePayment.objects.get_or_create(
                    student=s, fee_structure=fs,
                    defaults={
                        "amount_paid": random.choice([1200, 600, 0]),
                        "payment_date": today - timedelta(days=random.randint(1, 10)),
                        "status": random.choice(["PAID", "PENDING"]),
                    }
                )

        # --- Notices ---
        Notice.objects.get_or_create(
            title="Welcome to the new academic year!",
            defaults={
                "content": "We're excited to kick off 2025-2026. Please check your class schedules.",
                "audience": "ALL", "posted_by": admin, "is_pinned": True,
            }
        )
        Notice.objects.get_or_create(
            title="Staff meeting this Friday",
            defaults={
                "content": "All teachers are requested to attend the staff meeting at 3 PM.",
                "audience": "TEACHERS", "posted_by": admin,
            }
        )

        self.stdout.write(self.style.SUCCESS("Demo data seeded successfully!"))
