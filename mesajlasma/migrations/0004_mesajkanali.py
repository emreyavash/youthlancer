# Generated by Django 4.0.1 on 2022-05-13 00:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mesajlasma', '0003_remove_mesaj_user_mesaj_receiver_user_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='MesajKanali',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room', models.CharField(blank=True, max_length=50)),
                ('receiver_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='receiver1', to=settings.AUTH_USER_MODEL)),
                ('sender_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sender1', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
