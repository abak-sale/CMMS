# inventory/models.py
from django.db import models

class SparePart(models.Model):
    part_number = models.CharField(max_length=100, unique=True, verbose_name="Part Number / SKU")
    name = models.CharField(max_length=200, verbose_name="Nama Suku Cadang")
    stock = models.IntegerField(default=0, verbose_name="Stok Saat Ini")
    min_stock = models.IntegerField(default=5, verbose_name="Stok Minimum (Alert)")
    
    # PERBAIKAN: Menggunakan help_text sebagai ganti placeholder untuk panduan pengisian
    location = models.CharField(max_length=100, blank=True, null=True, help_text="Contoh: Rak A-02", verbose_name="Lokasi Rak")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']
        verbose_name = "Spare Part"

    def __str__(self):
        return f"{self.name} ({self.part_number}) - Stok: {self.stock}"

    @property
    def is_low_stock(self):
        return self.stock <= self.min_stock