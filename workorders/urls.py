# workorders/urls.py
from django.urls import path
from . import views

app_name = 'workorders'

urlpatterns = [
    path('dashboard/', views.cmms_dashboard, name='dashboard'),
    path('wo/<int:pk>/', views.workorder_detail, name='wo_detail'),
]