# Generated by Django 4.0.1 on 2022-03-25 09:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('isler', '0007_remove_i̇sbilgileri_resim_is_fotograf'),
    ]

    operations = [
        migrations.AddField(
            model_name='i̇sbilgileri',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
    ]
