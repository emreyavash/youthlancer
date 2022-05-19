from django.db import models
from django.contrib.auth.models import User
from isler.models import İsBilgileri
# Create your models here.

class ToplamBakiye(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    cekilen_para=  models.PositiveIntegerField(default=0)
    odenen_para=  models.PositiveIntegerField(default=0)
    toplam_bakiye = models.PositiveIntegerField(default=0)

class ParaCekme(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    cekilen_tutar = models.PositiveIntegerField()
    cekilme_tarihi = models.DateTimeField(auto_now_add=True)
    iban = models.CharField(max_length=11 ,null=True)

class ParaYatirma(models.Model):
    isveren = models.ForeignKey(User,related_name='para_isverene',on_delete=models.CASCADE)
    freelancer = models.ForeignKey(User,related_name='para_freelancer',on_delete=models.CASCADE)
    yapilan_is = models.ForeignKey(İsBilgileri,on_delete=models.CASCADE)
    yatırılan_tutar = models.PositiveIntegerField()
    yatirilma_tarihi = models.DateTimeField(auto_now_add=True)