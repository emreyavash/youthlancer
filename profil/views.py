from multiprocessing import context
from django.shortcuts import redirect, render
from .models import Kullanici,Sehir,Universite,Yetenekler,Yetenek_Kullanici,Portfoy_Kullanici,Fotograf_Kullanici
from django.contrib.auth.models import User
# Create your views here.

def profil_view(request,username):
    user = User.objects.get(username = username)
    kullanici = Kullanici.objects.filter(user = user)
    if kullanici.exists():
        kullanici = Kullanici.objects.get(user = user)
        kullanici_yetenek = Yetenek_Kullanici.objects.filter(user = user)
        portfolyo =Portfoy_Kullanici.objects.filter(user = user)
        fotograflar = Fotograf_Kullanici.objects.filter(user = user)
        if kullanici_yetenek.exists() or portfolyo.exists() or fotograflar.exists():
            context={
            'kullanici_yetenek':kullanici_yetenek,
            'kullanici':kullanici,
            'portfolyo':portfolyo,
            'fotograflar':fotograflar,
            'fotograf_sayi':fotograflar.count()
            }
            return render(request,'profil/profil.html',context)
        context={
            'yetenek_yazi':"Yetenek Eklenmemiş",
            'portfolyo_yazi':'Portfolyo Eklenmemiş',
            'fotograf_yazi':'Fotograf Eklenmemiş',
            'kullanici':kullanici,
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

def yetenek_ekle(request,username):
    yetenekler = Yetenekler.objects.all()
    user = User.objects.get(username = username)
    kullanici_yetenek = Yetenek_Kullanici.objects.filter(user=user)
    
    if request.method == "POST":
        yetenek_id = request.POST['yetenek']
        yetenek_seviye = request.POST['yetenek_seviye']
        yetenek = Yetenekler.objects.get(id = yetenek_id)
        if yetenek_seviye == "":
            return redirect('yetenekEkle',username)
        else:
            yetenek_var_mi = Yetenek_Kullanici.objects.filter(user = user).filter(yetenek = yetenek)
            if yetenek_var_mi.exists():
                context = {
                'yetenekler':yetenekler,
                'kullanici_yetenek':kullanici_yetenek,
                'error':'Daha önce eklendi',
                }
                return render(request,"profil/yetenek-ekle.html",context)
            else:
                yetenek_kayit = Yetenek_Kullanici.objects.create(user = user, yetenek_seviye = yetenek_seviye,yetenek = yetenek)
                yetenek_kayit.save()
                return redirect('yetenekEkle',username)
                
            
    if kullanici_yetenek.exists():
        context = {
            'yetenekler':yetenekler,
            'kullanici_yetenek':kullanici_yetenek,

        }
        return render(request,"profil/yetenek-ekle.html",context)
    else:
        context = {
            'yetenekler':yetenekler,
            'yetenek_yazi':"Yetenek Eklenmedi",

        }
        return render(request,"profil/yetenek-ekle.html",context)

def yetenek_sil(request,username,id):
    user = User.objects.get(username = username)
    Yetenek_Kullanici.objects.filter(user = user).filter(yetenek = id).delete()
    return redirect("yetenekEkle",username)

def portfoy_ekle(request,username):
    user = User.objects.get(username = username)
    portfoy = Portfoy_Kullanici.objects.filter(user = user)
    
    if request.method == "POST":
        aciklama = request.POST['portfolyo_aciklama']
        fotograf = request.FILES['portfoy_foto']

        if aciklama == " " or fotograf == " ":
            return redirect("portfoyEkle",username)
        else:
            portfoy_kayit = Portfoy_Kullanici.objects.create(user = user,aciklama = aciklama,fotograf = fotograf)
            portfoy_kayit.save()
            return redirect('portfoyEkle',username)
    else:
        if portfoy.exists():
            context={
                'portfoy':portfoy
            }
            return render(request,'profil/portfolyo-ekle.html',context)
        else:
            context={
                'portfoy_bos':'Portfoy Eklenmedi.'
            }
            return render(request,'profil/portfolyo-ekle.html',context)
            
def portfoy_sil(request,username,id):
    user = User.objects.get(username = username)
    Portfoy_Kullanici.objects.filter(user = user).filter(id = id).delete()
    return redirect("portfoyEkle",username)

def fotograf_ekle(request,username):
    user = User.objects.get(username = username)
    fotograf = Fotograf_Kullanici.objects.filter(user = user)
    if request.method == "POST":
        fotograf = request.FILES["fotograf"]
        if fotograf == " ":
            return redirect('fotografEkle',username)
        else:
            fotograf_kayit = Fotograf_Kullanici.objects.create(user = user,fotograf = fotograf)
            fotograf_kayit.save()
            return redirect('fotografEkle',username)

    else:
        if fotograf.exists():
            context={
                'fotograf':fotograf,
            }
            return render(request,"profil/fotograf-ekle.html",context)
        else:
            context={
                'fotograf_yazi':"Fotograf Eklenmedi.",
            }
            return render(request,"profil/fotograf-ekle.html",context)

def fotograf_sil(request,username,id):
    user = User.objects.get(username = username)
    Fotograf_Kullanici.objects.filter(user = user).filter(id = id).delete()
    return redirect("fotografEkle",username)
