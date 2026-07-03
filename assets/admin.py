# assets/admin.py
from django.contrib import admin
from .models import Asset

@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    # Memperbarui kolom yang muncul di halaman admin Django
    list_display = ('equipment_id', 'equipment_name', 'model_type', 'location')
    
    # Memperbarui fitur pencarian agar mencakup lokasi baru
    search_fields = ('equipment_id', 'equipment_name', 'serial_number', 'location')
    
    # Menghapus list_filter karena 'area' berbasis choices sudah tidak ada