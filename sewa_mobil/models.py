from django.db import models
from django.utils.text import slugify
from django.db.models import Q
from django.contrib.auth.models import User

from django_userforeignkey.models.fields import UserForeignKey

from django.contrib.contenttypes.fields import GenericRelation

from star_ratings.models import Rating

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

    ratings = GenericRelation(Rating, related_query_name='mobil')

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

    pesanan_dibuat = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    tgl_pesan = models.DateField()

    tgl_kembali = models.DateField()

    denda = models.FloatField(blank=True, null=True)
    
    total = models.IntegerField(blank=True, null=True)

    approved = models.BooleanField(blank=True, null=True, default=False)

    selesai = models.BooleanField(blank=True, null=True)

    tanggal_selesai = models.DateField(blank=True, null=True)

    def save(self, *args, **kwargs):
        date_format = "%Y-%m-%d"
        pesan = datetime.datetime.strptime(str(self.tgl_pesan), date_format)
        kembali = datetime.datetime.strptime(str(self.tgl_kembali), date_format)
        delta = kembali - pesan


        self.harga = abs(delta.days * self.mobil.harga)

        if self.selesai:

            dipulangkan = str(datetime.datetime.now().strftime(date_format))
            dipulangkan = datetime.datetime.strptime(dipulangkan, date_format)

            if kembali != dipulangkan:

                self.denda = 0.3

                # Hari pengembalian - kepulangan
                delta_ = dipulangkan - kembali

                hari = delta_.days 

                # Mendapatkan denda perbanyaknya hari terlambat
                perhari = hari * self.denda

                ntotal = self.harga * perhari
    
                self.total = abs(self.harga + ntotal)

                self.tanggal_selesai = datetime.datetime.now().strftime(date_format)

            else:
                self.denda = 0
                self.total = self.harga

        super(Pesanan, self).save(*args, **kwargs)

    def __str__(self):

        if self.selesai and self.approved:
            return '{}({}) - {} - STATUS: Selesai'.format(self.nama,self.mobil, self.user)

        elif self.approved:
            return '{}({}) - {} - STATUS: Sedang dipakai'.format(self.nama,self.mobil, self.user)

        else: 
            return '{}({}) - {} - STATUS: Menunggu Konfirmasi'.format(self.nama,self.mobil, self.user)
            

    

class Testimoni(models.Model):
    mobil = models.ForeignKey(Mobil, on_delete=models.CASCADE)
    nama = models.ForeignKey(User, on_delete=models.CASCADE)
    isi = models.TextField()
    dibuat_pada = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    
    class Meta:
        ordering = ['-dibuat_pada']

    def __str__(self):
        return f'Testimoni {self.isi} oleh {self.nama}'
