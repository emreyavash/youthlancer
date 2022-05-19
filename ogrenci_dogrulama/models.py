from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.

class OgrenciDogrulama(models.Model):
    ogrenci_belge=models.ImageField(upload_to='ogrenci')
    kullanici = models.ForeignKey(User,on_delete=models.CASCADE)
    date= models.DateTimeField(default=datetime.now())
    is_correct = models.BooleanField(default=False)
