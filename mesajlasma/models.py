from django.db import models
from django.contrib.auth.models import User
from profil.models import Kullanici
# Create your models here.
class MesajKanali(models.Model):
    room = models.CharField(max_length=50,blank=True)
    sender_user = models.ForeignKey(Kullanici,related_name='sender1',on_delete=models.CASCADE,null=True)
    receiver_user = models.ForeignKey(Kullanici,related_name='receiver1',on_delete=models.CASCADE,null=True)
    def __str__(self):
        return self.room
class Mesaj(models.Model):
    room = models.CharField(max_length=50,blank=True)
    sender_user = models.ForeignKey(Kullanici,related_name='sender',on_delete=models.CASCADE,null=True)
    receiver_user = models.ForeignKey(Kullanici,related_name='receiver',on_delete=models.CASCADE,null=True)
    mesaj = models.TextField()
    mesaj_tarih = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('mesaj_tarih',)
    def __str__(self):
        return self.mesaj