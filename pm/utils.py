# pm/utils.py
from datetime import date
from dateutil.relativedelta import relativedelta # Jika belum ada, jalankan: pip install python-dateutil
from .models import PreventiveSchedule
from workorders.models import WorkOrder

def trigger_preventive_maintenance():
    today = date.today()
    due_schedules = PreventiveSchedule.objects.filter(is_active=True, next_due_date__lte=today)
    
    generated_count = 0

    for schedule in due_schedules:
        formatted_date = today.strftime('%Y%m%d')
        wo_no = f"PM-WO-{formatted_date}-{schedule.asset.equipment_id}"
        
        if not WorkOrder.objects.filter(wo_number=wo_no).exists():
            WorkOrder.objects.create(
                wo_number=wo_no,
                title=f"[PM Berkala] {schedule.activity_name}",
                description=f"Tiket diterbitkan otomatis oleh sistem PM berkala untuk aset {schedule.asset.equipment_id}.",
                asset=schedule.asset,
                priority=WorkOrder.PriorityChoices.MEDIUM,
                status=WorkOrder.StatusChoices.CREATED
            )
            generated_count += 1

        # Hitung maju tanggal jatuh tempo berikutnya
        if schedule.frequency == PreventiveSchedule.FrequencyChoices.WEEKLY:
            schedule.next_due_date += relativedelta(weeks=1)
        elif schedule.frequency == PreventiveSchedule.FrequencyChoices.MONTHLY:
            schedule.next_due_date += relativedelta(months=1)
        elif schedule.frequency == PreventiveSchedule.FrequencyChoices.QUARTERLY:
            schedule.next_due_date += relativedelta(months=3)
        elif schedule.frequency == PreventiveSchedule.FrequencyChoices.SEMI_ANNUALLY:
            schedule.next_due_date += relativedelta(months=6)
        elif schedule.frequency == PreventiveSchedule.FrequencyChoices.ANNUALLY:
            schedule.next_due_date += relativedelta(years=1)
        
        schedule.save()
        
    return generated_count