# workorders/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import WorkOrder
from .forms import WorkOrderForm
from pm.utils import trigger_preventive_maintenance
from inventory.models import SparePart 

def cmms_dashboard(request):
    # Logika Trigger Tombol PM Manual
    if 'trigger_pm' in request.GET:
        count = trigger_preventive_maintenance()
        if count > 0:
            messages.success(request, f"Sukses! {count} Work Order berkala (PM) otomatis diterbitkan.")
        else:
            messages.info(request, "Pemeriksaan Selesai: Tidak ada jadwal PM yang jatuh tempo hari ini.")
        return redirect('workorders:dashboard')

    # Penanganan Form Input Tiket Manual
    if request.method == 'POST':
        form = WorkOrderForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Tiket Work Order baru berhasil dirilis!")
            return redirect('workorders:dashboard')
    else:
        form = WorkOrderForm()

    # Perhitungan Metrik KPI Dashboard
    work_orders = WorkOrder.objects.all().order_by('-id')
    total_wo = work_orders.count()
    active_wo = work_orders.filter(status__in=['CREATED', 'IN_PROGRESS']).count()
    breakdown_count = work_orders.filter(priority='EMERGENCY').count()
    
    # Kalkulasi total jam downtime
    total_downtime = sum(wo.downtime_hours for wo in work_orders if wo.downtime_hours)

    # Ambil data Spare Part yang stoknya kritis (Low Stock)
    all_parts = SparePart.objects.all()
    low_stock_parts = [part for part in all_parts if part.is_low_stock]

    context = {
        'work_orders': work_orders,
        'total_wo': total_wo,
        'active_wo': active_wo,
        'breakdown_count': breakdown_count,
        'total_downtime': total_downtime,
        'form': form,
        'low_stock_parts': low_stock_parts,
    }
    return render(request, 'workorders/dashboard.html', context)


def wo_detail(request, pk):
    """Fungsi Controller untuk Halaman Detail Tiket Work Order"""
    work_order = get_object_or_404(WorkOrder, pk=pk)
    
    # Mengambil semua riwayat pemakaian spare part khusus untuk WO ini
    consumptions = work_order.part_consumptions.all()
    
    context = {
        'work_order': work_order,
        'consumptions': consumptions,
    }
    return render(request, 'workorders/wo_detail.html', context)