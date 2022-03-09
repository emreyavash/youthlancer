from distutils.command.upload import upload
from django.db import models
from kategori.models import Kategori,AltKategori
from django.utils.text import slugify
# Create your models here.
class İsBilgileri(models.Model):
    is_isim=models.CharField(max_length=100)
    fiyat=models.IntegerField()
    resim=models.ImageField(upload_to='is')
    is_aciklama=models.TextField()
    kategori=models.ForeignKey(Kategori,on_delete=models.DO_NOTHING)
    alt_kategori=models.ForeignKey(AltKategori,on_delete=models.DO_NOTHING)
    is_baslangic= models.DateField()
    is_bitis= models.DateField()
    slug = models.SlugField(null=False,blank=True,unique=True,db_index=True,editable=False)


    def __str__(self):
        return f"{self.is_isim}"
    def save(self,*args, **kwargs):
        self.slug = slugify(self.is_isim)
        super().save(*args, **kwargs)