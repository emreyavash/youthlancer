from multiprocessing import context
from django.shortcuts import redirect, render
from .models import Kullanici,Sehir,Universite
from django.contrib.auth.models import User
# Create your views here.

def profil_view(request,username):
    user = User.objects.get(username = username)
    kullanici = Kullanici.objects.filter(user = user)
    if kullanici.exists():
        kullanici = Kullanici.objects.get(user = user)
        context={
            'kullanici':kullanici
        }
        return render(request,'profil/profil.html',context)
    else:
        return hesapAyarlari_view(request,username)

def hesapAyarlari_view(request,username):
    universite = Universite.objects.all()
    sehir = Sehir.objects.all()
    user = User.objects.get(username=username)
    kullanici = Kullanici.objects.filter(user=user)

    if request.method == "POST":
        
        if kullanici.exists():
            kullanici_bilgileri = Kullanici.objects.get(user=user)
            kullanici_bilgileri.kullanici_profil = request.FILES.get("profil-foto",False)
            kullanici_bilgileri.aciklama = request.POST["aciklama"]
            kullanici_bilgileri.dogum_gunu = request.POST['dogum_gunu']
            sehir_id = request.POST['sehir']
            universite_id = request.POST['universite']
            kullanici_bilgileri.sehir =Sehir.objects.get(id=sehir_id)
            kullanici_bilgileri.universite = Universite.objects.get(id = universite_id)
            kullanici_bilgileri.save()
            context={
                'sehirler':sehir,
                'universite':universite,
                'kullanici':kullanici_bilgileri
            }
            return render(request,'profil/hesapayarlari.html',context)
        else:
            profil_foto = request.FILES.get("profil-foto",False)
            aciklama = request.POST["aciklama"]
            sehir = request.POST['sehir']
            universite = request.POST['universite']
            dogum_gunu = request.POST["dogum_gunu"]
            sehir_id =Sehir.objects.get(id=sehir)
            universite_id = Universite.objects.get(id = universite)

            kullanici = Kullanici.objects.create(kullanici_profil = profil_foto,aciklama=aciklama,sehir=sehir_id,universite=universite_id,user=user,dogum_gunu =dogum_gunu)
            kullanici.save()
        
            return redirect('hesap-ayarlari',username)
    else:
        if kullanici.exists():
            kullanici_bilgileri = Kullanici.objects.get(user=user)

            context={
                'sehirler':sehir,
                'universite':universite,
                'kullanici':kullanici_bilgileri
            }
            return render(request,'profil/hesapayarlari.html',context)
        else:
            context={
                'sehirler':sehir,
                'universite':universite,
                
                'error':'Profil Bilgilerini Doğrulamadan Profiliniz Gözükmez.'
            }
            return render(request,'profil/hesapayarlari.html',context)

