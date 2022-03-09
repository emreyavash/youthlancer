from multiprocessing import context
from django.shortcuts import render
from kategori.models import Kategori
# Create your views here.


def anasayfa_view(request):
  
    return render(request,"anasayfa/icerik.html")

