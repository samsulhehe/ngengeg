from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from .views import index_view, about_view, contact_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index_view, name="home"),
    path('rent/', include('sewa_mobil.urls')),
    path('accounts/', include('akun.urls')),
    path('about/', about_view, name="about"),
    path('contact/', contact_view, name="contact"),
] 

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

