# Generated by Django 4.0.1 on 2022-03-20 14:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('profil', '0005_yetenekler'),
    ]

    operations = [
        migrations.CreateModel(
            name='Yetenek_Kullanici',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('yetenek_seviye', models.SmallIntegerField()),
                ('user', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
                ('yetenek', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.DO_NOTHING, to='profil.yetenekler')),
            ],
        ),
    ]
