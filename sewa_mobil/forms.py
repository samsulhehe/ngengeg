from django import forms

from .models import Pesanan

class FormPesanan(forms.ModelForm):
    class Meta:
        model = Pesanan
        fields = ['nama', 'mobil', 'KTP', 'KK', 'tgl_pesan', 'tgl_kembali']
