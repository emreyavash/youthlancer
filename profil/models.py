from distutils.command.upload import upload
from pyexpat import model
from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
# Create your models here.

class Sehir(models.Model):
    sehir = models.CharField(max_length=50)
    def __str__(self) :
        return f"{self.sehir}"

class Universite(models.Model):
    universite = models.CharField(max_length=150)
    status= models.SmallIntegerField(null=True)
    def __str__(self) :
        return f"{self.universite}"
class Kullanici(models.Model):
    user=models.ForeignKey(User,on_delete=models.DO_NOTHING,null=False,blank=True)
    kullanici_profil=models.ImageField(upload_to='kullanici',null=True)
    dogum_gunu = models.DateField(null=True)
    freelancer = models.BooleanField(default=False)
    telefon = models.IntegerField(null=True)
    isveren = models.BooleanField(default=False)
    sehir = models.ForeignKey(Sehir,on_delete=models.SET_NULL,null=True)
    universite = models.ForeignKey(Universite,on_delete=models.SET_NULL,null=True)
    aciklama = models.TextField()
    slug = models.SlugField(null=False,blank=True,unique=True,db_index=True,editable=False)
    def __str__(self) :
        return f"{self.user.first_name} {self.user.last_name}"
    def save(self,*args, **kwargs):
        self.slug = slugify(self.user.first_name,self.user.last_name)
        super().save(*args, **kwargs)

class Yetenekler(models.Model):
    ad = models.CharField(max_length=200)
    
class Yetenek_Kullanici(models.Model):
    user=models.ForeignKey(User,on_delete=models.DO_NOTHING,null=False,blank=True)
    yetenek = models.ForeignKey(Yetenekler,on_delete=models.DO_NOTHING,null=False,blank=True) 
    yetenek_seviye = models.SmallIntegerField()

class Portfoy_Kullanici(models.Model):
    user=models.ForeignKey(User,on_delete=models.DO_NOTHING,null=False,blank=True)
    aciklama = models.TextField()
    fotograf = models.ImageField(upload_to='portfoy',null=True)

class Fotograf_Kullanici(models.Model):
    user=models.ForeignKey(User,on_delete=models.DO_NOTHING,null=False,blank=True)
    fotograf = models.ImageField(upload_to='fotograf',null=True)