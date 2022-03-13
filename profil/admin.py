from django.contrib import admin
from .models import Universite,Kullanici,Sehir
# Register your models here.

admin.site.register(Kullanici)
admin.site.register(Universite)
admin.site.register(Sehir)