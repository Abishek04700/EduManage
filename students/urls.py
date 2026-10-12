from django.urls import path

from . import views

app_name = 'students'

urlpatterns = [
    path('', views.StudentListView.as_view(), name='list'),
    path('add/', views.student_create, name='create'),
    path('<int:pk>/', views.StudentDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', views.student_update, name='update'),
    path('<int:pk>/delete/', views.StudentDeleteView.as_view(), name='delete'),
]
