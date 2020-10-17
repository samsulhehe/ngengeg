# Generated by Django 3.1.2 on 2020-10-17 15:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_userforeignkey.models.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sewa_mobil', '0012_auto_20201017_1332'),
    ]

    operations = [
        migrations.CreateModel(
            name='Testimoni',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('isi', models.TextField()),
                ('dibuat_pada', models.DateTimeField(auto_now_add=True)),
                ('mobil', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sewa_mobil.mobil')),
                ('nama', django_userforeignkey.models.fields.UserForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['dibuat_pada'],
            },
        ),
    ]