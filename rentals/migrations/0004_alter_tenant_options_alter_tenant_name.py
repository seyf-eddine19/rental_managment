# Generated by Django 5.0.7 on 2025-02-08 20:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rentals', '0003_remove_activetenant_deposit_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tenant',
            options={'verbose_name': 'المستاجر', 'verbose_name_plural': 'المستاجرين'},
        ),
        migrations.AlterField(
            model_name='tenant',
            name='name',
            field=models.CharField(max_length=100, verbose_name='اسم المستاجر'),
        ),
    ]
