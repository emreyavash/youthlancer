# Generated by Django 4.0.1 on 2022-05-12 23:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mesajlasma', '0002_alter_mesaj_room'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mesaj',
            name='user',
        ),
        migrations.AddField(
            model_name='mesaj',
            name='receiver_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='receiver', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='mesaj',
            name='sender_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sender', to=settings.AUTH_USER_MODEL),
        ),
    ]