from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class OgrenciDogrulama(models.Model):
    ogrenci_belge=models.ImageField(upload_to='ogrenci')
    kullanici = models.ForeignKey(User,on_delete=models.CASCADE)
    date= models.DateTimeField(auto_now_add=True)
    is_correct = models.BooleanField(default=False)
