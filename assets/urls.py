# assets/urls.py
from django.urls import path
from . import views

app_name = 'assets'

urlpatterns = [
    path('', views.AssetListView.as_view(), name='asset_list'),
    path('import/', views.import_assets_excel, name='import_excel'),
]