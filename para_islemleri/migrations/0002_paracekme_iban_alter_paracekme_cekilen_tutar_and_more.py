# Generated by Django 4.0.1 on 2022-05-18 09:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('para_islemleri', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='paracekme',
            name='iban',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='paracekme',
            name='cekilen_tutar',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='parayatirma',
            name='yatırılan_tutar',
            field=models.PositiveIntegerField(),
        ),
    ]
