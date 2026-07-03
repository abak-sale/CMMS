# workorders/admin.py
from django.contrib import admin
from .models import WorkOrder

@admin.register(WorkOrder)
class WorkOrderAdmin(admin.ModelAdmin):
    list_display = ('wo_number', 'title', 'asset', 'priority', 'status', 'created_at')