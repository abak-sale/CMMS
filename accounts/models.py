# accounts/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    # Mendefinisikan Role/Peran di dalam CMMS
    class Role(models.TextChoices):
        ADMIN = 'ADMIN', 'Administrator'
        PLANNER = 'PLANNER', 'Maintenance Planner'
        TECHNICIAN = 'TECHNICIAN', 'Maintenance Technician'

    # Menambahkan field role ke dalam model user dengan default TECHNICIAN
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.TECHNICIAN
    )
    
    # Field tambahan opsional untuk pelacakan performa teknisi nanti
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"