# inventory/admin.py
from django.contrib import admin
from .models import SparePart

@admin.register(SparePart)
class SparePartAdmin(admin.ModelAdmin):
    list_display = ('part_number', 'name', 'stock', 'min_stock', 'location', 'is_low_stock')
    list_filter = ('location',)
    search_fields = ('part_number', 'name')