from django import forms

from .models import Mobil, Pesanan, Testimoni

class FormPesanan(forms.ModelForm):
    class Meta:
        model = Pesanan
        fields = ['nama', 'mobil', 'KTP', 'KK', 'tgl_pesan', 'tgl_kembali']

class FormTestimoni(forms.ModelForm):
    class Meta:
        model = Testimoni
        fields = ['isi']
