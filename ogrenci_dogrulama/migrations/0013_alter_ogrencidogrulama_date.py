# Generated by Django 4.0.1 on 2022-05-18 20:22

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ogrenci_dogrulama', '0012_alter_ogrencidogrulama_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ogrencidogrulama',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 5, 18, 23, 22, 40, 571607)),
        ),
    ]
