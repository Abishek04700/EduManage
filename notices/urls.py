from django.urls import path

from . import views

app_name = 'notices'

urlpatterns = [
    path('', views.NoticeListView.as_view(), name='list'),
    path('add/', views.notice_form_view, name='create'),
    path('<int:pk>/edit/', views.notice_form_view, name='update'),
    path('<int:pk>/delete/', views.NoticeDeleteView.as_view(), name='delete'),
]
