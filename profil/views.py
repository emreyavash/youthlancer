
from django.contrib import messages
from django.shortcuts import redirect, render

from .models import Kullanici,Sehir,Universite,Yetenekler,Yetenek_Kullanici,Portfoy_Kullanici,Fotograf_Kullanici,UploadFile
from isler.models import Secilen_Freelancer,İsBilgileri,Kategori,İsGereksinimleri,AltKategori
from django.contrib.auth.models import User
from isler.models import Basvuru_Kayitlari,Secilen_Freelancer
from ogrenci_dogrulama.models import OgrenciDogrulama
from ogrenci_dogrulama.views import ogrenci_dogrulama,dogrulama
from para_islemleri.models import ParaYatirma,ToplamBakiye
from para_islemleri.views import para_yatirma 

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime

# Create your views here.
@login_required(login_url='giris_yap')
def profil_view(request,username):
    
    user = User.objects.get(username = username)
    kullanici = Kullanici.objects.filter(Q(user = user),Q(hesap_kayit = True))
    isveren_profil = Secilen_Freelancer.objects.filter(Q(user = request.user.id),Q(is_veren = user.id))
    try:
        giris_yapan_kullanici = Kullanici.objects.get(user = request.user.id)
    except ObjectDoesNotExist:
        return hesapAyarlari_view(request,username)
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
                    'user_mi':user,
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
                'user_mi':user,
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
        kullanici = Kullanici.objects.filter(Q(user=user),Q(hesap_kayit = True))
        ogrenci_belgesi = OgrenciDogrulama.objects.filter(kullanici = user.id)
        if request.method == "POST":
            
            if kullanici.exists():
                kullanici_bilgileri = Kullanici.objects.get(user=user)
                if request.FILES.get("profil-foto") is None:
                    kullanici_bilgileri.kullanici_profil = request.POST["hidden_profil_fotografi"]
                else:
                    kullanici_bilgileri.kullanici_profil = request.FILES["profil-foto"]
                kullanici_bilgileri.aciklama = request.POST["aciklama"]
                kullanici_bilgileri.dogum_gunu = request.POST['dogum_gunu']
                sehir_id = request.POST['sehir']
                universite_id = request.POST['universite']
                kullanici_bilgileri.sehir =Sehir.objects.get(id=sehir_id)
                kullanici_bilgileri.universite = Universite.objects.get(id = universite_id)
                kullanici_bilgileri.hesap_kayit = True
                kullanici_bilgileri.save()
                if  ogrenci_belgesi.exists() == False:
                    if request.FILES.get("ogrenci_belge") is not None:
                        ogrenci_belge = request.FILES["ogrenci_belge"]
                        dogrulama(ogrenci_belge,user.username)
                context={
                    'sehirler':sehir,
                    'universite':universite,
                    'kullanici':kullanici_bilgileri,
                    'user':user,
                }
                return redirect('hesap-ayarlari',user.username)
            else:
                kullanici_bilgileri = Kullanici.objects.get(user=user)
                if request.FILES.get("profil-foto") is None:
                    kullanici_bilgileri.kullanici_profil = request.POST["hidden_profil_fotografi"]
                else:
                    kullanici_bilgileri.kullanici_profil = request.FILES["profil-foto"]
                kullanici_bilgileri.aciklama = request.POST["aciklama"]
                kullanici_bilgileri.dogum_gunu = request.POST['dogum_gunu']
                sehir_id = request.POST['sehir']
                universite_id = request.POST['universite']
                kullanici_bilgileri.sehir =Sehir.objects.get(id=sehir_id)
                kullanici_bilgileri.universite = Universite.objects.get(id = universite_id)
                kullanici_bilgileri.hesap_kayit = True
                kullanici_bilgileri.save()
                if  ogrenci_belgesi.exists() == False:
                    if request.FILES.get("ogrenci_belge") is not None:
                        ogrenci_belge = request.FILES["ogrenci_belge"]
                        dogrulama(ogrenci_belge,user.username)
                context={
                    'sehirler':sehir,
                    'universite':universite,
                    'kullanici':kullanici_bilgileri,
                    'user':user,
                }
                return redirect('hesap-ayarlari',user.username)
        else:
            if kullanici.exists():
                kullanici_bilgileri = Kullanici.objects.get(user=user)
                try:
                    belge_onay = OgrenciDogrulama.objects.get(kullanici = user)
                except ObjectDoesNotExist:
                    belge_onay = None
                context={
                    'sehirler':sehir,
                    'universite':universite,
                    'kullanici':kullanici_bilgileri,
                    'user':user,
                    'belge_onay':belge_onay

                }
                return render(request,'profil/hesapayarlari.html',context)
            else:
                context={
                    'sehirler':sehir,
                    'universite':universite,
                    'user':user,
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
    return redirect('paylasilan_isler',username)
@login_required(login_url='giris_yap')
def is_duzenle(request,username,id):
    user = User.objects.get(username=username)
    is_bilgileri = İsBilgileri.objects.get(Q(user = user.id),Q(id = id))
    kategori = Kategori.objects.all()
    alt_kategori = AltKategori.objects.filter(is_active=True)
    is_gereksinimleri = İsGereksinimleri.objects.all()
    if request.method == 'POST':
        is_bilgileri.is_isim = request.POST["is_isim"]
        is_bilgileri.fiyat = int(request.POST['fiyat'])
        is_bilgileri.is_aciklama = request.POST['aciklama']
        if request.FILES.get('isfoto1') is None:
            is_bilgileri.resim1 = request.POST['hidden_resim1']
        else:
            is_bilgileri.resim1 = request.FILES['isfoto1']
        if request.FILES.get('isfoto2') is None:
            is_bilgileri.resim2 = request.POST['hidden_resim2']
        else:
            is_bilgileri.resim2 = request.FILES['isfoto2']
        if request.FILES.get('isfoto3') is None:
            is_bilgileri.resim3 = request.POST['hidden_resim3']
        else:
            is_bilgileri.resim3 = request.FILES['isfoto3']
        is_bilgileri.is_baslangic = request.POST['baslangic']
        is_bilgileri.is_bitis = request.POST['bitis']
        is_bilgileri.kategori_id = request.POST['kategori']
        is_bilgileri.alt_kategori_id = request.POST['alt_kategori']
        is_bilgileri.is_gereksinimleri = request.POST['is_gereksinimleri']
        is_bilgileri.is_active  = request.POST.get('is_active')
        is_bilgileri.guncelleme_tarihi = datetime.now()
        is_bilgileri.save()
        
        is_db = İsBilgileri.objects.get(is_isim = is_bilgileri.is_isim)
       
        return redirect('icerik',is_db.slug) 

    else:
        context={
            'kategori':kategori,
            'alt_kategori':alt_kategori,
            'is_gereksinimleri':is_gereksinimleri,
            'is_bilgileri':is_bilgileri,
        }
    return render(request,'profil/is_duzenle.html',context)

@login_required(login_url='giris_yap')
def biten_isler(request,username):
    if request.user.username == username:
        kullanici = User.objects.get(username = username)
        kullanici_bilgileri = Kullanici.objects.get(user = kullanici.id)
        if kullanici_bilgileri.freelancer:
            biten_isler = Secilen_Freelancer.objects.filter(Q(user = kullanici.id),Q(is_bitti_mi = True))

        if kullanici_bilgileri.isveren:   
            biten_isler = Secilen_Freelancer.objects.filter(Q(is_veren = kullanici.id),Q(is_bitti_mi = True))
            for biten_is in biten_isler:
                
                    odeme_yapildi_mi = ParaYatirma.objects.filter(freelancer = biten_is.user,isveren = biten_is.is_veren,yapilan_is = biten_is.is_bilgi)
                    if odeme_yapildi_mi.exists():
                       odeme_yapildi_mi= odeme_yapildi_mi.first()
                    else:
                        odeme_yapildi_mi = None
                        para_yatirma(request,is_id=biten_is.is_bilgi,username=biten_is.is_veren.username)
                
        if biten_isler.exists():
            context={
                'biten_isler':biten_isler,
                'kullanici':kullanici,
                'odeme_yapildi_mi':odeme_yapildi_mi
            }
        else:
            context={
            'kullanici':kullanici,

            'error':'Biten iş yok.'
            }
        return render(request,'profil/biten_isler.html',context)
    else:
        return redirect('anasayfa') 

@login_required(login_url='giris_yap')
def aldigin_isler(request,username):
    if request.user.username == username:
        kullanici = User.objects.get(username = username)
        kullanici2 = Kullanici.objects.get(user = kullanici.id)
        secilen_free = Secilen_Freelancer.objects.filter(user_id = kullanici.id).exclude(is_bitti_mi = True)
        if secilen_free.exists():
            if request.method == 'POST':
                if request.FILES.get('teslim_et') is None:
                    pass
                else:
                    is_bilgi_id = request.POST['is_bilgi']
                    freelancer_id = request.POST['freelancer'] 
                    isveren_id = request.POST['isveren'] 
                    is_bilgi = İsBilgileri.objects.get(id = int(is_bilgi_id))
                    freelancer = User.objects.get(id = freelancer_id)
                    isveren = User.objects.get(id = isveren_id)
                    upload_file = request.FILES['teslim_et']
                    UploadFile.objects.create(is_bilgi = is_bilgi.id,freelancer = freelancer,isveren= isveren,file=upload_file )
                    upload = UploadFile.objects.get(Q(is_bilgi = is_bilgi.id),Q(freelancer = freelancer),Q(isveren = isveren))
                    yapılan_is = Secilen_Freelancer.objects.get(Q(is_bilgi = is_bilgi),Q(user = freelancer),Q(is_veren = isveren))
                    yapılan_is.is_bitti_mi = True
                    yapılan_is.upload = upload
                    yapılan_is.save()
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

@login_required(login_url='giris_yap')
def basvuran_freelancerlar(request,username):
    user = User.objects.get(username = username)
    if request.user.username == username:
     
      
        secilen_freelancer = Secilen_Freelancer.objects.filter(is_veren = user)
        if secilen_freelancer.exists():

            basvuran_freelancerlar = Basvuru_Kayitlari.objects.filter(Q(is_veren = user),Q(secildi_mi = False)).exclude(Q(is_bilgi__in = secilen_freelancer.values_list('is_bilgi')))
        else:
            basvuran_freelancerlar = Basvuru_Kayitlari.objects.filter(Q(is_veren = user),Q(secildi_mi = False))

        context = {
            'basvuran_freelancerlar':basvuran_freelancerlar,
            'secilen_freelancer':secilen_freelancer,
            'secilen_freelancer_var_mi':secilen_freelancer.exists(),
            
        }
        return render(request,'profil/basvuran_freelancerlar.html',context)
    else:
        return redirect('anasayfa')

def basvuran_freelancer_onay(request,is_id,user_id):
    basvurulan_is= Basvuru_Kayitlari.objects.get(Q(is_bilgi = is_id),Q(user=user_id))
    basvurulan_is.secildi_mi=True
    basvurulan_is.save()
    freelancer_secim = Secilen_Freelancer.objects.create(user = basvurulan_is.user,is_bilgi = basvurulan_is.is_bilgi,secildi_mi =1,is_bitti_mi=0,basvuru_id=basvurulan_is.id,is_veren = basvurulan_is.is_bilgi.user)
    freelancer_secim.save()
    return redirect('kabul_edilen_freelancerlar',basvurulan_is.is_bilgi.user.username)

def basvuran_freelancer_iptal(request,is_id,user_id):
    Basvuru_Kayitlari.objects.get(Q(is_bilgi = is_id),Q(user=user_id)).delete()
    
    return redirect('basvuran_freelancerlar',request.user.username)


@login_required(login_url='giris_yap')
def kabul_edilen_freelancerlar(request,username):
    if request.user.username == username:

        user = User.objects.get(username = username)
        secilen_freelancer = Secilen_Freelancer.objects.filter(Q(is_veren = user))
        context = {
            'user':user,
            'secilen_freelancer':secilen_freelancer
        }
        return render(request,'profil/kabul_edilen_freelancerlar.html',context)
    else:
        return redirect('anasayfa')

def kabul_edilen_freelancer_onay(request,is_id,user_id):
    basvurulan_is= Basvuru_Kayitlari.objects.get(Q(is_bilgi = is_id),Q(user=user_id))
    
    freelancer_secim = Secilen_Freelancer.objects.create(user = basvurulan_is.user,is_bilgi = basvurulan_is.is_bilgi,secildi_mi =1,is_bitti_mi=0,basvuru_id=basvurulan_is.id,is_veren = basvurulan_is.is_bilgi.user)
    freelancer_secim.save()

    return redirect('kabul_edilen_freelancerlar',basvurulan_is.is_bilgi.user.username)
def kabul_edilen_freelancer_iptal(request,is_id,id):
    basvurulan_is = Basvuru_Kayitlari.objects.get(Q(is_bilgi = is_id), Q(user = id))
    basvurulan_is.secildi_mi = False
    basvurulan_is.save()
    freelancer_iptal = Secilen_Freelancer.objects.get(Q(is_bilgi = is_id), Q(user = id))
    freelancer_iptal.delete()
    return redirect('kabul_edilen_freelancerlar',freelancer_iptal.is_bilgi.user.username)

def hesap_ozeti(request,username):
    user  =User.objects.get(username = username)
    if request.user.username == user.username:
        kullanici = Kullanici.objects.get (user = user.id)
        try:
            bakiye = ToplamBakiye.objects.get(user = user.id)
        except ObjectDoesNotExist:
            bakiye = None
        context = {
            'kullanici':kullanici,
            'bakiye':bakiye
        }
        return render(request,'profil/hesap_ozeti.html',context)
    else:
        return redirect('anasayfa')

