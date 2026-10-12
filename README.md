# EduManage — Student Management System

A full-featured, role-based Student Management System built with Django. Designed for schools to manage students, teachers, courses, attendance, exams, fees, and notices from a single, professional dashboard.

## Features

- **Role-based access control** — Admin, Teacher, and Student roles each get a tailored dashboard and permission set
- **Student & Teacher management** — full CRUD with profile photos, guardian info, employment details
- **Academics** — manage academic years, classes/courses, and subjects, with class-teacher and subject-teacher assignment
- **Attendance** — mark daily attendance per class in bulk, view history, weekly attendance chart on the admin dashboard
- **Exams & Results** — create exams per class, enter marks per subject, automatic percentage & letter-grade calculation
- **Fees** — define fee structures per class, record and track payments with status (Paid / Pending / Overdue)
- **Notice board** — post announcements targeted at everyone, teachers only, or students only
- **Django Admin** — every model is fully registered and customized for power-user management
- **Clean, professional UI** — custom sidebar layout, Inter/Sora typography, Bootstrap 5 + Chart.js, not a generic template

## Tech Stack

- **Backend:** Django 6.1 (Python)
- **Database:** SQLite (default, swappable for PostgreSQL/MySQL in production)
- **Frontend:** Django Templates + Bootstrap 5 + Bootstrap Icons + Chart.js
- **Forms:** django-crispy-forms with crispy-bootstrap5

## Project Structure

```
sms_project/       # Project settings and root URLs
accounts/          # Custom User model, auth, role-based dashboards
academics/         # Academic years, courses/classes, subjects
students/          # Student profiles and CRUD
teachers/          # Teacher profiles and CRUD
attendance/        # Daily attendance marking & history
exams/              # Exams and results with auto-grading
fees/               # Fee structures and payment tracking
notices/            # Notice board
templates/          # All HTML templates (base layout + per-app templates)
static/             # Custom CSS
```

## Getting Started

### 1. Clone and set up a virtual environment

```bash
git clone <your-repo-url>
cd sms
python3 -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment variables

```bash
cp .env.example .env
# Edit .env and set a real SECRET_KEY for production
```

### 4. Run migrations

```bash
python manage.py migrate
```

### 5. Seed demo data (optional but recommended)

This creates an admin account, 3 teachers, 12 students, sample courses/subjects, a week of attendance, exam results, and fee records.

```bash
python manage.py seed_demo_data
```

Demo credentials created:

| Role    | Username    | Password    |
|---------|-------------|-------------|
| Admin   | `admin`     | `admin123`  |
| Teacher | `teacher1`  | `teacher123`|
| Student | `student1`  | `student123`|

### 6. Run the development server

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` and log in.

## Roles & Permissions

- **Admin** — full access to every module, including Django Admin (`/admin/`)
- **Teacher** — manage students, mark attendance, enter exam results, post notices
- **Student** — read-only dashboard: own attendance, results, and fee status

## Roadmap Ideas

- Email notifications for fee due dates and low attendance
- Parent portal
- PDF report card generation
- REST API for a mobile app

## License

MIT — feel free to use this as a foundation for your own school management project.
