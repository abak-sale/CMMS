# assets/models.py
from django.db import models

class Asset(models.Model):
    # 1. Equipment ID (Harus unik)
    equipment_id = models.CharField(max_length=50, unique=True, verbose_name="Equipment ID")
    
    # 2. Equipment Name
    equipment_name = models.CharField(max_length=100, verbose_name="Equipment Name")
    
    # 3. Type / Model
    model_type = models.CharField(max_length=100, verbose_name="Type / Model")
    
    # 4. Serial Number
    serial_number = models.CharField(max_length=100, blank=True, null=True, verbose_name="Serial Number")
    
    # 5. Capacity
    capacity = models.CharField(max_length=50, blank=True, null=True, verbose_name="Capacity")
    
    # 6. Area & Location (Digabung menjadi satu field tekstual yang fleksibel)
    location = models.CharField(max_length=255, verbose_name="Area & Location")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.equipment_id} - {self.equipment_name}"