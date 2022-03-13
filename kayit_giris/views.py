from django.shortcuts import render

# Create your views here.

def kayit_ol(request):
    return render(request,"kayit_giris/kayitol.html")

def giris_yap(request):
    return render(request,"kayit_giris/girisyap.html")