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

    harga = models.IntegerField(blank=True, null=True)

    tgl_pesan = models.DateField()

    tgl_kembali = models.DateField()

    denda = models.IntegerField(blank=True, null=True)

    total = models.IntegerField(blank=True, null=True)

    selesai = models.BooleanField(default=False, blank=True)

    approved = models.BooleanField(default=False, blank=True)

    def __str__(self):
        return '{}({}) - {}-APPROVED:{}'.format(self.nama,self.mobil, self.user, self.approved)



    

