from django.urls import path

from . import views

app_name = 'fees'

urlpatterns = [
    path('structures/', views.FeeStructureListView.as_view(), name='structure_list'),
    path('structures/add/', views.fee_structure_form_view, name='structure_create'),
    path('structures/<int:pk>/edit/', views.fee_structure_form_view, name='structure_update'),
    path('structures/<int:pk>/delete/', views.FeeStructureDeleteView.as_view(), name='structure_delete'),

    path('payments/', views.FeePaymentListView.as_view(), name='payment_list'),
    path('payments/add/', views.fee_payment_form_view, name='payment_create'),
    path('payments/<int:pk>/edit/', views.fee_payment_form_view, name='payment_update'),
    path('payments/<int:pk>/delete/', views.FeePaymentDeleteView.as_view(), name='payment_delete'),
]
