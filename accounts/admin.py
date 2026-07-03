# accounts/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    # Menampilkan field tambahan di halaman detail admin
    fieldsets = UserAdmin.fieldsets + (
        ('Informasi CMMS', {'fields': ('role', 'phone_number')}),
    )
    
    # Menampilkan kolom ini pada daftar user di admin
    list_display = ['username', 'email', 'role', 'is_staff']

# Daftarkan CustomUser menggunakan konfigurasi CustomUserAdmin
admin.site.register(CustomUser, CustomUserAdmin)