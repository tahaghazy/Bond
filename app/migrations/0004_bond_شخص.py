# Generated by Django 3.0.9 on 2020-12-05 20:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_auto_20201205_1749'),
    ]

    operations = [
        migrations.AddField(
            model_name='bond',
            name='شخص',
            field=models.CharField(default=8, max_length=50),
        ),
    ]
