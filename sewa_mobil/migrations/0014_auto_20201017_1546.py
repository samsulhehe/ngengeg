# Generated by Django 3.1.2 on 2020-10-17 15:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sewa_mobil', '0013_testimoni'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pesanan',
            name='denda',
            field=models.FloatField(blank=True, null=True),
        ),
    ]