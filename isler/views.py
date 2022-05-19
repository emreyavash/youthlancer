from distutils.log import error
from django.shortcuts import redirect, render
from kategori.models import Kategori,AltKategori
from isler.models import İsBilgileri,İsGereksinimleri,Basvuru_Kayitlari,Secilen_Freelancer
from profil.models import Universite,Sehir,Kullanici
from django.contrib.auth.models import User

from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.
def filtering(param):
    return param != '' and param is not None

def isler_view(request,slug):

    kategori = Kategori.objects.get(slug=slug)
    is_filter = İsBilgileri.objects.filter(Q(kategori=kategori.id),Q(is_active = True)).order_by('id').reverse()
    alt_kategori = AltKategori.objects.filter(kategori=kategori.id)
    try:
        kullanici = Kullanici.objects.get(user = request.user.id)
    except Kullanici.DoesNotExist:
        kullanici=None
    if is_filter.exists():
        
        altkategori = request.GET.get('alt-kategori')
        min_fiyat = request.GET.get('min_fiyat')
        max_fiyat = request.GET.get('max_fiyat')
        if filtering(altkategori):
            altkategoriFilter = AltKategori.objects.get(altKategoriAd = altkategori)
            is_filter = is_filter.filter(alt_kategori = altkategoriFilter.id)

        if filtering(min_fiyat):
            is_filter = is_filter.filter(fiyat__gte=min_fiyat) 

        if filtering(max_fiyat):
            is_filter = is_filter.filter(fiyat__lte=max_fiyat) 

        if is_filter.exists():

            context={
                'is':is_filter,
                'kategoriListe':kategori,
                'altKategori':alt_kategori,
                'kullanici':kullanici
            }
            return render(request,"isler/isler.html",context)

        else:
            context={
                'error':'İş Yok',
                'kategoriListe':kategori,
                'altKategori':alt_kategori,
                'kullanici':kullanici
            }
            return render(request,"isler/isler.html",context)


    else:
        context={
            'error':'İş Yok',
            'kategoriListe':kategori,
            'altKategori':alt_kategori,
            'kullanici':kullanici


        }
        return render(request,"isler/isler.html",context)

def is_olustur(request,username): # İş Fotoğrafları, iş gereksinimleri iyileştirelecek
    # eğer aynı isimli iş varsa hata mesajı gönder
    user = User.objects.get(username=username)
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
        isbilgi_kayit = İsBilgileri.objects.create(is_isim = is_isim, fiyat =fiyat,is_aciklama=aciklama,resim1 = foto1, resim2=foto2,resim3=foto3,is_baslangic = baslangic,is_bitis=bitis,kategori_id = kategori_ad,alt_kategori_id=alt_kategori,user=user)
        isbilgi_kayit.save()
        is_db = İsBilgileri.objects.get(is_isim = is_isim)
       
        return redirect('icerik',is_db.slug) 

    else:
        context={
            'kategori':kategori,
            'alt_kategori':alt_kategori,
            'is_gereksinimleri':is_gereksinimleri,
        }
    return render(request,'isler/is-olustur.html',context)

def icerik_view(request,slug):

    is_bilgileri = İsBilgileri.objects.get(slug=slug)
    basvuranlar = Basvuru_Kayitlari.objects.filter(is_bilgi = is_bilgileri.id)
    tum_basvurular = Basvuru_Kayitlari.objects.all()
    for i in tum_basvurular:
        secilmis_freelancer = Secilen_Freelancer.objects.filter(user = i.user.id).first()
        
    try:
        is_onaylandi_mi = Secilen_Freelancer.objects.get(is_bilgi=is_bilgileri.id)
    except ObjectDoesNotExist:
        is_onaylandi_mi= None
    if request.user.is_authenticated:
        basvuran = Basvuru_Kayitlari.objects.filter(Q(is_bilgi = is_bilgileri.id) , Q(user = request.user.id)).exists()

        basvuru = Secilen_Freelancer.objects.filter(user = request.user.id).filter(is_bitti_mi = False).exists()
       
        try:
            kullanici = Kullanici.objects.get(user = request.user)
        except ObjectDoesNotExist:
            kullanici= None
    else:
        kullanici= None
        basvuru = None
        basvuran = None
        
    if basvuranlar.exists():
        
        context={
            'is':is_bilgileri,
            'user_bilgi':request.user,
            'basvuranlar':basvuranlar,
            'is_onay':is_onaylandi_mi,
            'kullanici':kullanici,
            'basvuru_error':basvuru,
            'basvuran':basvuran,
            'secilmis_freelancer':secilmis_freelancer
        }
       
    else:
        context={
            'is':is_bilgileri,
            'user_bilgi':request.user,
            'error':'Başvuran Kullanıcı Bulunmamaktadır.',
            'kullanici':kullanici,
            'basvuru_error':basvuru,
            'basvuran':basvuran,

        }
    return render(request,'isler/isicerik.html',context)

def basvur_view(request,slug):
    is_bilgi= İsBilgileri.objects.get(slug=slug)
    user_info = Kullanici.objects.get(user=request.user.id)
    
    if request.method == 'POST':
       
        alan=request.POST['alan']
        secim_aciklama=request.POST['secim_aciklama']
   
        basvuru_kayit = Basvuru_Kayitlari.objects.create(user_id = request.user.id,alan=alan,secim_aciklama=secim_aciklama,is_bilgi_id=is_bilgi.id,kullanici_bilgi_id = user_info.id,is_veren = is_bilgi.user)
        basvuru_kayit.save()
        return redirect('icerik',slug)
    context ={
        'is':is_bilgi,
    
        'user_info':user_info,
    }
    return render(request,'isler/basvur.html',context)



