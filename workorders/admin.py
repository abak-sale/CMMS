# workorders/admin.py
from django.contrib import admin
from .models import WorkOrder, WorkOrderPartConsumption

class WorkOrderPartConsumptionInline(admin.TabularInline):
    model = WorkOrderPartConsumption
    extra = 1 # Menyediakan 1 baris kosong otomatis untuk input part

@admin.register(WorkOrder)
class WorkOrderAdmin(admin.ModelAdmin):
    list_display = ('wo_number', 'title', 'asset', 'priority', 'status', 'downtime_hours')
    list_filter = ('priority', 'status')
    search_fields = ('wo_number', 'title')
    inlines = [WorkOrderPartConsumptionInline] # Masukkan fungsi input part di dalam detail WO