# Generated by Django 4.0.1 on 2022-03-13 16:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profil', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='universite',
            name='status',
            field=models.SmallIntegerField(null=True),
        ),
    ]