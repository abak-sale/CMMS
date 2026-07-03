# config/urls.py
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('assets/', include('assets.urls')),
    path('workorders/', include('workorders.urls')),
    
    # UBAH permanent MENJADI False (Menggunakan HTTP 302 Temporary Redirect)
    path('', RedirectView.as_view(url='/workorders/dashboard/', permanent=False)),
]