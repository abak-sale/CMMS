# workorders/views.py
from pm.utils import trigger_preventive_maintenance
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Sum
from .models import WorkOrder
from .forms import WorkOrderForm, WorkOrderUpdateStatusForm

def cmms_dashboard(request):
    # Logika Trigger Tombol PM Manual
    if 'trigger_pm' in request.GET:
        count = trigger_preventive_maintenance()
        if count > 0:
            messages.success(request, f"Sukses! {count} Work Order berkala (PM) otomatis diterbitkan.")
        else:
            messages.info(request, "Pemeriksaan Selesai: Tidak ada jadwal PM yang jatuh tempo hari ini.")
        return redirect('workorders:dashboard')
    # Prosedur input tiket kerja baru jika user submit form
    if request.method == 'POST':
        form = WorkOrderForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Work Order baru berhasil diterbitkan ke lapangan!")
            return redirect('workorders:dashboard')
    else:
        form = WorkOrderForm()

    # Ambil seluruh data Work Order dari database
    work_orders = WorkOrder.objects.all()

    # Hitung metrik rangkuman untuk kotak dashboard (KPI)
    total_wo = work_orders.count()
    active_wo = work_orders.exclude(status=WorkOrder.StatusChoices.CLOSED).count()
    breakdown_count = work_orders.filter(priority=WorkOrder.PriorityChoices.EMERGENCY).count()
    
    # Hitung total kerugian jam downtime (jika kosong, otomatis set ke angka 0.0)
    total_downtime = work_orders.aggregate(Sum('downtime_hours'))['downtime_hours__sum'] or 0.0

    context = {
        'work_orders': work_orders,
        'form': form,
        'total_wo': total_wo,
        'active_wo': active_wo,
        'breakdown_count': breakdown_count,
        'total_downtime': total_downtime,
    }
    return render(request, 'workorders/dashboard.html', context)

def workorder_detail(request, pk):
    # Mengambil data 1 tiket WO berdasarkan ID-nya
    work_order = get_object_or_404(WorkOrder, pk=pk)
    
    if request.method == 'POST':
        form = WorkOrderUpdateStatusForm(request.POST, instance=work_order)
        if form.is_valid():
            form.save()
            messages.success(request, f"Progress tiket {work_order.wo_number} berhasil di-update.")
            return redirect('workorders:dashboard')
    else:
        form = WorkOrderUpdateStatusForm(instance=work_order)

    return render(request, 'workorders/wo_detail.html', {'work_order': work_order, 'form': form})