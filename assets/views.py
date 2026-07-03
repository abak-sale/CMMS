# assets/views.py
import pandas as pd
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import ListView # <-- Pastikan import ini ada
from .models import Asset
from .forms import ExcelImportForm

# 1. TAMBAHKAN KEMBALI KELAS INI YANG SEMPAT HILANG
class AssetListView(ListView):
    model = Asset
    template_name = 'assets/asset_list.html'
    context_object_name = 'assets'

# 2. Fungsi import fleksibel yang sudah kita buat sebelumnya (tetap pertahankan ini)
def import_assets_excel(request):
    if request.method == 'POST':
        form = ExcelImportForm(request.POST, request.FILES)
        if form.is_valid():
            excel_file = request.FILES['excel_file']
            
            try:
                df = pd.read_excel(excel_file)
                df.columns = [str(col).strip().lower() for col in df.columns]
                
                col_mapping = {}
                for col in df.columns:
                    if 'id' in col:
                        col_mapping['equipment_id'] = col
                    elif 'name' in col:
                        col_mapping['equipment_name'] = col
                    elif 'type' in col or 'model' in col:
                        col_mapping['model_type'] = col
                    elif 'serial' in col or 'sn' in col:
                        col_mapping['serial_number'] = col
                    elif 'capacity' in col or 'kapasitas' in col:
                        col_mapping['capacity'] = col
                    elif 'location' in col or 'area' in col or 'lokasi' in col:
                        col_mapping['location'] = col

                required_keys = ['equipment_id', 'equipment_name', 'model_type', 'location']
                if not all(k in col_mapping for k in required_keys):
                    messages.error(
                        request, 
                        "Format kolom Excel tidak dikenali. Pastikan memiliki header: "
                        "Equipment ID, Equipment Name, Type/Model, Serial Number, Capacity, Area & Location"
                    )
                    return render(request, 'assets/import_excel.html', {'form': form})

                success_count = 0
                
                for index, row in df.iterrows():
                    raw_id = row[col_mapping['equipment_id']]
                    eq_id = str(raw_id).strip() if not pd.isna(raw_id) else ""
                    
                    if eq_id == "" or eq_id.lower() == 'nan':
                        continue
                    
                    raw_name = row[col_mapping['equipment_name']]
                    raw_type = row[col_mapping['model_type']]
                    
                    sn_val = str(row[col_mapping['serial_number']]).strip() if 'serial_number' in col_mapping and not pd.isna(row[col_mapping['serial_number']]) else None
                    cap_val = str(row[col_mapping['capacity']]).strip() if 'capacity' in col_mapping and not pd.isna(row[col_mapping['capacity']]) else None
                    loc_val = str(row[col_mapping['location']]).strip() if 'location' in col_mapping and not pd.isna(row[col_mapping['location']]) else "Pabrik"

                    Asset.objects.update_or_create(
                        equipment_id=eq_id,
                        defaults={
                            'equipment_name': str(raw_name).strip() if not pd.isna(raw_name) else "Tanpa Nama",
                            'model_type': str(raw_type).strip() if not pd.isna(raw_type) else "General",
                            'serial_number': sn_val,
                            'capacity': cap_val,
                            'location': loc_val,
                        }
                    )
                    success_count += 1
                
                messages.success(request, f"Berhasil mengimpor {success_count} data aset generator ke dalam database.")
                return redirect('assets:asset_list')
                
            except Exception as e:
                messages.error(request, f"Terjadi kesalahan teknis saat membaca berkas: {str(e)}")
    else:
        form = ExcelImportForm()
        
    return render(request, 'assets/import_excel.html', {'form': form})