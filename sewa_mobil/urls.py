from django.urls import path, include

from .views import car_list, detail_view, pesanan_view, batal_pesan

urlpatterns = [
            path('', car_list, name="list"),
            path('pesan/', pesanan_view, name="pesan"),
            path('detail/<slug>', detail_view, name="detail"),
            path('batal/', batal_pesan, name="batal"),
        ]
