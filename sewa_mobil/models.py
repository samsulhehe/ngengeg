from django.db import models
from django.utils.text import slugify

from django_userforeignkey.models.fields import UserForeignKey

import datetime

class Mobil(models.Model):
    nama = models.CharField(max_length=100, default="")

    plat = models.CharField(max_length=10, default="")

    gambar = models.ImageField(upload_to='img/mobil/')

    gambar2 = models.ImageField(upload_to='img/mobil/')
    
    gambar3 = models.ImageField(upload_to='img/mobil/')

    gambar4 = models.ImageField(upload_to='img/mobil/', blank=True)

    ditambahkan = models.DateTimeField(auto_now_add=True)

    kategori = [
        ('Covertible', 'Covertible'),
        ('Coupe', 'Coupe'),
        ('Sedan', 'Sedan'),
        ('Hatchback', 'Hatchback'),
        ('SUV', 'SUV'),
        ('MPV', 'MPV'),
    ]

    tipe = models.CharField(max_length=20, choices=kategori, default="MPV")

    harga = models.IntegerField(default=100000)

    deskripsi = models.TextField()

    status_choices = [
        ('Available', 'Available'),
        ('Not Available', 'Not Available'),
    ]

    transmisi = models.CharField(max_length=10, default="Manual", choices=[('Auto', 'Auto'),('Manual', 'Manual')])

    status = models.CharField(max_length=20, choices=status_choices, default="Available")

    slug = models.SlugField(blank=True, editable=False)

    class Meta:
        ordering = ["harga"]

    def save(self, *args, **kwargs):
        super(Mobil, self).save(*args, **kwargs)
        self.slug = slugify(self.plat)
        super().save()

    def __str__(self):

        if self.status == "Available":
            return f'{self.nama}({self.plat})'
        else:
            return f'{self.nama}({self.plat}) (TIDAK TERSEDIA)'


class Pesanan(models.Model):
    nama = models.CharField(max_length=100, default="")

    user = UserForeignKey(auto_user_add=True)

    mobil = models.ForeignKey(Mobil, on_delete=models.CASCADE)

    KTP = models.ImageField(upload_to='img/ktp')

    KK = models.ImageField(upload_to='img/kk')

    harga = models.IntegerField(editable=False, null=True, blank=True)

    tgl_pesan = models.DateField()

    tgl_kembali = models.DateField()

    denda = models.FloatField(blank=True, null=True)

    total = models.IntegerField(blank=True, null=True)

    selesai_choice = (
            ('Menunggu Konfirmasi', 'Menunggu Konfirmasi'),
            ('Sedang Dipakai', 'Sedang Dipakai'),
            ('Selesai', 'Selesai'),
            )

    selesai = models.CharField(max_length=100, choices=selesai_choice, default="Menunggu Konfirmasi")

    approved = models.BooleanField(default=False, blank=True)

    def save(self, *args, **kwargs):
        date_format = "%Y-%m-%d"
        pesan = datetime.datetime.strptime(str(self.tgl_pesan), date_format)
        kembali = datetime.datetime.strptime(str(self.tgl_kembali), date_format)
        delta = kembali - pesan


        self.harga = abs(delta.days * self.mobil.harga)

        if self.selesai == "Selesai":

            dipulangkan = str(datetime.datetime.now().strftime(date_format))
            dipulangkan = datetime.datetime.strptime(dipulangkan, date_format)

            if kembali != dipulangkan:
                ndenda = dipulangkan - kembali

                self.denda = 0.3

                ntotal = self.harga * self.denda

                self.total = abs(self.harga + ntotal)
            else:
                self.denda = 0
                self.total = self.harga

        super(Pesanan, self).save(*args, **kwargs)

    def __str__(self):
        return '{}({}) - {}-APPROVED:{} - STATUS: {}'.format(self.nama,self.mobil, self.user, self.approved, self.selesai)
    

class Testimoni(models.Model):
    mobil = models.ForeignKey(Mobil, on_delete=models.CASCADE)
    nama = UserForeignKey(auto_user_add=True)
    isi = models.TextField()
    dibuat_pada = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['dibuat_pada']

    def __str__(self):
        return f'Komentar {self.isi} oleh {self.nama}'
