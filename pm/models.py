# pm/models.py
from django.db import models
from assets.models import Asset

class PreventiveSchedule(models.Model):
    class FrequencyChoices(models.TextChoices):
        WEEKLY = 'WEEKLY', 'Mingguan'
        MONTHLY = 'MONTHLY', 'Bulanan'
        QUARTERLY = 'QUARTERLY', '3 Bulanan (Kuartal)'
        SEMI_ANNUALLY = 'SEMI_ANNUALLY', '6 Bulanan'
        ANNUALLY = 'ANNUALLY', 'Tahunan'

    # Hubungkan ke master data Asset yang di-import dari Excel
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name='pm_schedules')
    activity_name = models.CharField(max_length=200)
    frequency = models.CharField(max_length=20, choices=FrequencyChoices.choices, default=FrequencyChoices.MONTHLY)
    next_due_date = models.DateField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['next_due_date']
        verbose_name = "Preventive Schedule"

    def __str__(self):
        return f"PM {self.asset.equipment_id} - {self.activity_name} ({self.get_frequency_display()})"