# Generated by Django 4.0.1 on 2022-03-18 18:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profil', '0002_universite_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='kullanici',
            name='protfoy',
        ),
        migrations.AddField(
            model_name='kullanici',
            name='dogum_gunu',
            field=models.DateField(null=True),
        ),
    ]
