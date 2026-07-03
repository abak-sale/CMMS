# workorders/models.py
from django.db import models
from django.conf import settings
from assets.models import Asset # Mengambil model Asset yang sudah sukses kita buat sebelumnya

class WorkOrder(models.Model):
    # 1. Pilihan Status Alur Kerja (Siklus Hidup Tiket)
    class StatusChoices(models.TextChoices):
        CREATED = 'CREATED', 'Created / Open'
        ASSIGNED = 'ASSIGNED', 'Assigned'
        IN_PROGRESS = 'IN_PROGRESS', 'In Progress'
        PENDING = 'PENDING', 'Pending / On Hold'
        COMPLETED = 'COMPLETED', 'Completed'
        CLOSED = 'CLOSED', 'Closed'

    # 2. Pilihan Tingkat Kedaruratan (Priority)
    class PriorityChoices(models.TextChoices):
        LOW = 'LOW', 'Low'
        MEDIUM = 'MEDIUM', 'Medium'
        HIGH = 'HIGH', 'High'
        EMERGENCY = 'EMERGENCY', 'Emergency / Breakdown'

    # --- Kolom-Kolom Tabel ---
    
    # Nomor Tiket Kerja (Contoh: WO-2026-0001)
    wo_number = models.CharField(max_length=50, unique=True, verbose_name="Work Order Number")
    
    # Judul Pekerjaan / Masalah Kerusakan
    title = models.CharField(max_length=200, verbose_name="Job Title")
    
    # Deskripsi Kronologi Kerusakan atau Instruksi Kerja
    description = models.TextField(verbose_name="Description / Instructions")
    
    # Relasi ke Tabel Aset (Mesin mana yang rusak)
    # models.PROTECT menjaga agar data riwayat WO tidak ikut terhapus jika data mesin tidak sengaja terhapus
    asset = models.ForeignKey(
        Asset, 
        on_delete=models.PROTECT, 
        related_name='work_orders',
        verbose_name="Asset ID"
    )
    
    # Dropdown Tingkat Prioritas
    priority = models.CharField(
        max_length=20, 
        choices=PriorityChoices.choices, 
        default=PriorityChoices.MEDIUM
    )
    
    # Dropdown Alur Status Kerja
    status = models.CharField(
        max_length=20, 
        choices=StatusChoices.choices, 
        default=StatusChoices.CREATED
    )
    
    # Jam Downtime/Kerugian Operasional akibat kerusakan mesin (Default 0.00 jam)
    downtime_hours = models.DecimalField(max_digits=5, decimal_places=2, default=0.00, verbose_name="Downtime (Hours)")
    
    # Tanggal otomatis saat tiket dibuat & diperbarui
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at'] # Tiket terbaru akan selalu muncul paling atas
        verbose_name = "Work Order"
        verbose_name_plural = "Work Orders"

    def __str__(self):
        return f"{self.wo_number} - {self.title} [{self.get_status_display()}]"