# Generated by Django 3.0.8 on 2020-10-14 11:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sewa_mobil', '0005_mobil_gambar4'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pesanan',
            name='harga',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]