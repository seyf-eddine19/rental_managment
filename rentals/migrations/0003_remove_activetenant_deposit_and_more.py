# Generated by Django 5.0.7 on 2025-02-07 18:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rentals', '0002_alter_apartment_options_alter_building_options_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='activetenant',
            name='deposit',
        ),
        migrations.RemoveField(
            model_name='activetenant',
            name='payment_status',
        ),
        migrations.RemoveField(
            model_name='rentalhistory',
            name='deposit',
        ),
        migrations.RemoveField(
            model_name='rentalhistory',
            name='payment_status',
        ),
        migrations.AlterField(
            model_name='activetenant',
            name='contract_number',
            field=models.CharField(max_length=50, unique=True, verbose_name='رقم العقد'),
        ),
        migrations.AlterField(
            model_name='building',
            name='building_number',
            field=models.CharField(max_length=3, unique=True, verbose_name='رقم العمارة'),
        ),
        migrations.AlterField(
            model_name='rentalhistory',
            name='active_tenant',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='rentals.activetenant', verbose_name='العقد الحالي'),
        ),
        migrations.AlterField(
            model_name='tenant',
            name='id_number',
            field=models.CharField(max_length=20, unique=True, verbose_name='رقم الهوية'),
        ),
        migrations.AlterField(
            model_name='tenant',
            name='phone_number',
            field=models.CharField(max_length=15, unique=True, verbose_name='رقم الهاتف'),
        ),
    ]
