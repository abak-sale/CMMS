# pm/admin.py
from django.contrib import admin
from .models import PreventiveSchedule

@admin.register(PreventiveSchedule)
class PreventiveScheduleAdmin(admin.ModelAdmin):
    # Kolom yang akan tampil di baris tabel admin
    list_display = ('asset', 'activity_name', 'frequency', 'next_due_date', 'is_active', 'created_at')
    
    # Fitur filter di sebelah kanan halaman admin
    list_filter = ('frequency', 'is_active', 'next_due_date')
    
    # Fitur pencarian berdasarkan ID mesin atau nama aktivitas
    search_fields = ('asset__equipment_id', 'activity_name')
    
    # Mengurutkan berdasarkan tanggal jatuh tempo terdekat
    ordering = ('next_due_date',)