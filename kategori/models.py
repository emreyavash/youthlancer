from tkinter import CASCADE
from django.db import models
from django.utils.text import slugify
# Create your models here.

class Kategori(models.Model):
    kategoriAd=models.CharField(max_length=50)
    slug=models.SlugField(null=False,blank=True,unique=True,db_index=True,editable=False)
    def __str__(self) :
        return f"{self.kategoriAd}"
    def save(self,*args, **kwargs):
        self.slug = slugify(self.kategoriAd)
        super().save(*args, **kwargs)

class AltKategori(models.Model):
    kategori=models.ForeignKey(Kategori,on_delete=models.CASCADE,null=False)
    altKategoriAd=models.CharField(max_length=50)
    slug = models.SlugField(null=False,blank=True,unique=True,db_index=True,editable=False)
    is_active = models.BooleanField(default=True)

    def __str__(self) :
            return f"{self.altKategoriAd}"
    def save(self,*args, **kwargs):
        self.slug = slugify(self.altKategoriAd)
        super().save(*args, **kwargs)