# Generated by Django 4.0.1 on 2022-03-25 23:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('isler', '0009_i̇sbilgileri_resim1_i̇sbilgileri_resim2_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='İsGereksinimleri',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gereksinim', models.CharField(max_length=100)),
            ],
        ),
    ]
