from django.urls import path

from . import views

app_name = 'academics'

urlpatterns = [
    path('courses/', views.CourseListView.as_view(), name='course_list'),
    path('courses/add/', views.course_form_view, name='course_create'),
    path('courses/<int:pk>/edit/', views.course_form_view, name='course_update'),
    path('courses/<int:pk>/delete/', views.CourseDeleteView.as_view(), name='course_delete'),

    path('subjects/', views.SubjectListView.as_view(), name='subject_list'),
    path('subjects/add/', views.subject_form_view, name='subject_create'),
    path('subjects/<int:pk>/edit/', views.subject_form_view, name='subject_update'),
    path('subjects/<int:pk>/delete/', views.SubjectDeleteView.as_view(), name='subject_delete'),
]
