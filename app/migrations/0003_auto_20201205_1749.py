# Generated by Django 3.0.9 on 2020-12-05 15:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20201201_1611'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bond',
            name='operation_number',
            field=models.CharField(error_messages={'unique': 'عزيزي الموظف رقم العمليه مكرر يرجى مراجعة البحث وشكرا.'}, max_length=10000, verbose_name='رقم العمليه'),
        ),
        migrations.AlterUniqueTogether(
            name='bond',
            unique_together={('shop', 'operation_number')},
        ),
    ]
