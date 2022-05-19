from django.db import models
from kategori.models import Kategori,AltKategori
from profil.models import Kullanici,UploadFile
from django.contrib.auth.models import User
from django.utils.text import slugify
from multiselectfield import MultiSelectField
# Create your models here.
class İsBilgileri(models.Model):
    is_isim=models.CharField(max_length=100)
    fiyat=models.PositiveSmallIntegerField(default=1)
    is_aciklama=models.TextField()
    kategori=models.ForeignKey(Kategori,on_delete=models.DO_NOTHING)
    alt_kategori=models.ForeignKey(AltKategori,on_delete=models.DO_NOTHING)
    resim1 = models.ImageField(upload_to="is_fotograf",null=True)
    resim2 = models.ImageField(upload_to="is_fotograf",null=True)
    resim3 = models.ImageField(upload_to="is_fotograf",null=True)
    is_baslangic= models.DateField()
    is_bitis= models.DateField()
    slug = models.SlugField(null=False,blank=True,unique=True,db_index=True,editable=False)
    user = models.ForeignKey(User,on_delete=models.DO_NOTHING,null=True)
    is_active = models.BooleanField(default=True)
    yayin_tarihi = models.DateTimeField(auto_now_add=True,null=True,blank=True,editable=False)
    guncelleme_tarihi = models.DateTimeField(auto_now=True,null=True,blank=True,editable=False)

    def __str__(self):
        return f"{self.is_isim}"
    def save(self,*args, **kwargs):
        self.slug = slugify(self.is_isim)
        super().save(*args, **kwargs)


class İsGereksinimleri(models.Model):
    gereksinim = models.CharField(max_length=100)
    def __str__(self):
        return f"{self.gereksinim}"
    def save(self,*args, **kwargs):
        self.slug = slugify(self.gereksinim)
        super().save(*args, **kwargs)

class Kullanici_Gereksinim(models.Model):
    is_bilgi=models.ForeignKey(İsBilgileri,on_delete=models.DO_NOTHING,null=True)
    gereksinim = MultiSelectField(İsGereksinimleri)


class Basvuru_Kayitlari(models.Model):
    user= models.ForeignKey(User,on_delete=models.CASCADE)
    is_bilgi = models.ForeignKey(İsBilgileri,on_delete=models.CASCADE)
    kullanici_bilgi = models.ForeignKey(Kullanici,on_delete=models.CASCADE)
    is_veren  =models.ForeignKey(User,related_name='isveren',on_delete=models.CASCADE,null=True)
    alan= models.CharField(max_length=100)
    secim_aciklama = models.TextField()
    secildi_mi = models.BooleanField(default=0)

    def __str__(self):
        return f'{self.user.username}'

class Secilen_Freelancer(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='freelancer')
    is_bilgi = models.ForeignKey(İsBilgileri,on_delete=models.CASCADE,related_name='is_id')
    basvuru = models.ForeignKey(Basvuru_Kayitlari,on_delete=models.CASCADE,null=True)
    is_veren = models.ForeignKey(User,on_delete=models.CASCADE,null=True,related_name='is_veren')
    secildi_mi= models.BooleanField(default=0)
    is_bitti_mi=models.BooleanField(default=0)
    upload = models.ForeignKey(UploadFile,on_delete=models.CASCADE,null=True)