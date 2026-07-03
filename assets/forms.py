# assets/forms.py
from django import forms

class ExcelImportForm(forms.Form):
    excel_file = forms.FileField(
        label="Pilih File Excel (.xlsx)",
        help_text="Format kolom wajib: Equipment ID, Equipment Name, Type/Model, Serial Number, Capacity, Area & Location"
    )

    def clean_excel_file(self):
        file = self.cleaned_data.get('excel_file')
        if not file.name.endswith('.xlsx'):
            raise forms.ValidationError("Format file harus berupa .xlsx (Excel)")
        return file