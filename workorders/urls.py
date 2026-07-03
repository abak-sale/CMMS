# workorders/urls.py
from django.urls import path
from . import views

app_name = 'workorders'

urlpatterns = [
    # Rute ke Dashboard Utama CMMS
    path('dashboard/', views.cmms_dashboard, name='dashboard'),
    
    # PERBAIKAN: Mengubah views.workorder_detail menjadi views.wo_detail agar sinkron dengan template
    path('wo/<int:pk>/', views.wo_detail, name='wo_detail'),
]