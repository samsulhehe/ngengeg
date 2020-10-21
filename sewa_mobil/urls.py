from django.urls import path, include

from .views import car_list, detail_view, pesanan_view, edit, delete_view

urlpatterns = [
            path('', car_list, name="list"),
            path('pesan/', pesanan_view, name="pesan"),
            path('edit', edit, name="edit"),
            path('delete', delete_view, name="delete"),
            path('detail/<slug>', detail_view, name="detail"),
        ]
