# Generated by Django 4.0.1 on 2022-05-16 21:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('isler', '0026_basvuru_kayitlari_is_veren'),
    ]

    operations = [
        migrations.AddField(
            model_name='basvuru_kayitlari',
            name='secildi_mi',
            field=models.BooleanField(default=0),
        ),
    ]