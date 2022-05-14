from multiprocessing import context
from django.shortcuts import redirect, render

from .models import Kullanici,Sehir,Universite,Yetenekler,Yetenek_Kullanici,Portfoy_Kullanici,Fotograf_Kullanici
from isler.models import Secilen_Freelancer,İsBilgileri,Kategori,İsGereksinimleri,AltKategori
from django.contrib.auth.models import User
from isler.models import Basvuru_Kayitlari,Secilen_Freelancer

from django.contrib.auth.decorators import login_required
from django.db.models import Q

# Create your views here.
@login_required(login_url='giris_yap')
def profil_view(request,username):
    
    user = User.objects.get(username = username)
    kullanici = Kullanici.objects.filter(user = user)
    giris_yapan_kullanici = Kullanici.objects.get(user = request.user.id)
    isveren_profil = Secilen_Freelancer.objects.filter(Q(user = request.user.id),Q(is_veren = user.id))
    if giris_yapan_kullanici.freelancer:
        if  user.username == request.user.username:
            if kullanici.exists():
                kullanici = Kullanici.objects.get(user = user)
                kullanici_yetenek = Yetenek_Kullanici.objects.filter(user = user)
                portfolyo =Portfoy_Kullanici.objects.filter(user = user)
                fotograflar = Fotograf_Kullanici.objects.filter(user = user)
    

                if kullanici_yetenek.exists() or portfolyo.exists() or fotograflar.exists():
                    context={
                    'user_mi':user,
                    'kullanici_yetenek':kullanici_yetenek,
                    'kullanici':kullanici,
                    'portfolyo':portfolyo,
                    'fotograflar':fotograflar,
                    'fotograf_sayi':fotograflar.count(),
                
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
        elif isveren_profil.exists():
                kullanici = Kullanici.objects.get(user = user)
                kullanici_yetenek = Yetenek_Kullanici.objects.filter(user = user)
                portfolyo =Portfoy_Kullanici.objects.filter(user = user)
                fotograflar = Fotograf_Kullanici.objects.filter(user = user)
    

                if kullanici_yetenek.exists() or portfolyo.exists() or fotograflar.exists():
                    context={
                    'user_mi':user,
                    'kullanici_yetenek':kullanici_yetenek,
                    'kullanici':kullanici,
                    'portfolyo':portfolyo,
                    'fotograflar':fotograflar,
                    'fotograf_sayi':fotograflar.count(),
                
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
            return redirect('anasayfa')
    else:
        if kullanici.exists():
            kullanici = Kullanici.objects.get(user = user)
            kullanici_yetenek = Yetenek_Kullanici.objects.filter(user = user)
            portfolyo =Portfoy_Kullanici.objects.filter(user = user)
            fotograflar = Fotograf_Kullanici.objects.filter(user = user)
    

            if kullanici_yetenek.exists() or portfolyo.exists() or fotograflar.exists():
                context={
                'user_mi':user,
                'kullanici_yetenek':kullanici_yetenek,
                'kullanici':kullanici,
                'portfolyo':portfolyo,
                'fotograflar':fotograflar,
                'fotograf_sayi':fotograflar.count(),
            
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

@login_required(login_url='giris_yap')
def hesapAyarlari_view(request,username):
    if request.user.username == username:

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
    else:
            return redirect('anasayfa')
@login_required(login_url='giris_yap')
def yetenek_ekle(request,username):
    if request.user.username == username:

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
    else:
            return redirect('anasayfa')
def yetenek_sil(request,username,id):
    user = User.objects.get(username = username)
    Yetenek_Kullanici.objects.filter(user = user).filter(yetenek = id).delete()
    return redirect("yetenekEkle",username)

@login_required(login_url='giris_yap')
def portfoy_ekle(request,username):
    if request.user.username == username:

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
    else:
            return redirect('anasayfa')

def portfoy_sil(request,username,id):
    user = User.objects.get(username = username)
    Portfoy_Kullanici.objects.filter(user = user).filter(id = id).delete()
    return redirect("portfoyEkle",username)
    
@login_required(login_url='giris_yap')
def fotograf_ekle(request,username):
    if request.user.username == username:

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
    else:
            return redirect('anasayfa')
def fotograf_sil(request,username,id):
    user = User.objects.get(username = username)
    Fotograf_Kullanici.objects.filter(user = user).filter(id = id).delete()
    return redirect("fotografEkle",username)
    
@login_required(login_url='giris_yap')
def basvurulan_isler(request,username):
    if request.user.username == username:
        kullanici = User.objects.get(username = username)
        kullanici2 = Kullanici.objects.get(user = kullanici.id)
        basvurulan_isler = Basvuru_Kayitlari.objects.filter(user_id = kullanici.id)
        if basvurulan_isler.exists():
            context={
                'basvurulan_isler':basvurulan_isler,
                'kullanici':kullanici,
                'kullanici2':kullanici2,
            }
        else:
            context={
            'basvurulan_isler':basvurulan_isler,
            'kullanici':kullanici,
            'kullanici2':kullanici2,

            'error':'Başvurulan iş yok.'
            }
        return render(request,'profil/basvurulan_isler.html',context)
    else:
        return redirect('anasayfa')

def basvuru_sil(request,id,username):
    user = User.objects.get(username = username)
    Basvuru_Kayitlari.objects.filter(is_bilgi = id).filter(user = user).delete()
    return redirect('basvurulan_isler',username)



@login_required(login_url='giris_yap')
def paylasilan_isler(request,username):
    if request.user.username == username:
        kullanici = User.objects.get(username = username)
        kullanici2 = Kullanici.objects.get(user = kullanici.id)
        paylasilan_isler = İsBilgileri.objects.filter(user_id = kullanici.id)
        

        if paylasilan_isler.exists():
    
                    
            context={
                    'paylasilan_isler':paylasilan_isler.order_by('id').reverse(),
                    'kullanici':kullanici,
                    'kullanici2':kullanici2,

                    }
                    

        else:
            context={
            'paylasilan_isler':paylasilan_isler.order_by('id').reverse(),
            'kullanici':kullanici,
            'kullanici2':kullanici2,

            'error':'Paylaşılan iş yok.'
            }
        return render(request,'profil/paylasilan_isler.html',context)
    else:
        return redirect('anasayfa')
def paylasilan_sil(request,id,username):
    user = User.objects.get(username = username)
    İsBilgileri.objects.filter(id = id).filter(user = user).delete()
    return redirect('basvurulan_isler',username)
@login_required(login_url='giris_yap')
def is_duzenle(request,username,id):
    user = User.objects.get(username=username)
    is_bilgileri = İsBilgileri.objects.get(Q(user = user.id),Q(id = id))
    kategori = Kategori.objects.all()
    alt_kategori = AltKategori.objects.filter(is_active=True)
    is_gereksinimleri = İsGereksinimleri.objects.all()
    if request.method == 'POST':
        is_isim = request.POST["is_isim"]
        fiyat = int(request.POST['fiyat'])
        aciklama = request.POST['aciklama']
        foto1 = request.FILES['isfoto1']
        foto2 = request.FILES['isfoto2']
        foto3 = request.FILES['isfoto3']
        baslangic = request.POST['baslangic']
        bitis = request.POST['bitis']
        kategori_ad = request.POST['kategori']
        alt_kategori = request.POST['alt_kategori']
        is_gereksinimleri = request.POST['is_gereksinimleri']
        isbilgi_kayit = İsBilgileri.objects.update(is_isim = is_isim, fiyat =fiyat,is_aciklama=aciklama,resim1 = foto1, resim2=foto2,resim3=foto3,is_baslangic = baslangic,is_bitis=bitis,kategori_id = kategori_ad,alt_kategori_id=alt_kategori,user=user)
        isbilgi_kayit.save()
        is_db = İsBilgileri.objects.get(is_isim = is_isim)
       
        return redirect('icerik',is_db.slug) 

    else:
        context={
            'kategori':kategori,
            'alt_kategori':alt_kategori,
            'is_gereksinimleri':is_gereksinimleri,
            'is_bilgileri':is_bilgileri,
        }
    return render(request,'profil/is_duzenle.html',context)

def biten_isler(request,username):
    if request.user.username == username:
        kullanici = User.objects.get(username = username)
        biten_isler = Basvuru_Kayitlari.objects.filter(user_id = kullanici.id)
        if biten_isler.exists():
            context={
                'basvurulan_isler':biten_isler,
                'kullanici':kullanici,
            }
        else:
            context={
            'basvurulan_isler':biten_isler,
            'kullanici':kullanici,

            'error':'Biten iş yok.'
            }
        return render(request,'profil/biten_isler.html',context)
    else:
        return redirect('anasayfa') 


def aldigin_isler(request,username):
    if request.user.username == username:
        kullanici = User.objects.get(username = username)
        kullanici2 = Kullanici.objects.get(user = kullanici.id)
        secilen_free = Secilen_Freelancer.objects.filter(user_id = kullanici.id)
        if secilen_free.exists():
            context={
                'secilen_free':secilen_free,
                'kullanici':kullanici,
                'kullanici2':kullanici2,
            }
        else:
            context={
            'secilen_free':secilen_free,
            'kullanici':kullanici,
            'kullanici2':kullanici2,

            'error':'Alınan iş yok.'
            }
        return render(request,'profil/aldigin-isler.html',context)
    else:
        return redirect('anasayfa')