# workorders/forms.py
from django import forms
from .models import WorkOrder

class WorkOrderForm(forms.ModelForm):
    class Meta:
        model = WorkOrder
        # Kita panggil kolom-kolom yang mau diinput oleh user
        fields = ['wo_number', 'title', 'description', 'asset', 'priority']
        widgets = {
            'wo_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contoh: WO-2026-0001'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nama kerusakan / aktivitas'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Kronologi masalah...'}),
            'asset': forms.Select(attrs={'class': 'form-select'}),
            'priority': forms.Select(attrs={'class': 'form-select'}),
        }

class WorkOrderUpdateStatusForm(forms.ModelForm):
    class Meta:
        model = WorkOrder
        fields = ['status', 'downtime_hours']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select'}),
            'downtime_hours': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
        }