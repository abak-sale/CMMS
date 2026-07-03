# config/urls.py
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('assets/', include('assets.urls')),
    path('workorders/', include('workorders.urls')),
    path('pm/', include('pm.urls')), # <-- Tambahkan baris ini!
    
    path('', RedirectView.as_view(url='/workorders/dashboard/', permanent=False)),
]