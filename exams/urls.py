from django.urls import path

from . import views

app_name = 'exams'

urlpatterns = [
    path('', views.ExamListView.as_view(), name='list'),
    path('add/', views.exam_form_view, name='create'),
    path('<int:pk>/', views.ExamDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', views.exam_form_view, name='update'),
    path('<int:pk>/delete/', views.ExamDeleteView.as_view(), name='delete'),
    path('<int:exam_id>/add-result/', views.result_entry, name='add_result'),
]
