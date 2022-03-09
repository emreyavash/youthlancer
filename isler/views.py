from tkinter.tix import MAX
from django.shortcuts import render
from kategori.models import Kategori,AltKategori
from isler.models import İsBilgileri
from django.db.models import Max,Min
# Create your views here.

def isler_view(request,slug):

    kategori = Kategori.objects.get(slug=slug)
    is_filter = İsBilgileri.objects.filter(kategori=kategori.id)
    alt_kategori = AltKategori.objects.filter(kategori=kategori.id)
    if is_filter.exists():
        if request.method == "POST":
            
            if 'alt-kategori' in request.POST:
                altkategori = request.POST['alt-kategori']
                altKategori = AltKategori.objects.get(altKategoriAd = altkategori)
                is_altkategori= İsBilgileri.objects.filter(alt_kategori = altKategori.id)
                context={
                    'is':is_altkategori,
                    'kategoriListe':kategori,
                    'altKategori':alt_kategori,
                    'isvar':True,
                
                    
                }
                return render(request,"isler/isler.html",context)
            elif 'max_fiyat' in request.POST :
                max_fiyat =int(request.POST['max_fiyat'])
                is_min = İsBilgileri.objects.filter(kategori=kategori.id).order_by('fiyat').first()
                is_fiyat = İsBilgileri.objects.filter(kategori=kategori.id).filter(fiyat__range=(is_min.fiyat,max_fiyat))
                context={
                    'is':is_fiyat,
                    'kategoriListe':kategori,
                    'altKategori':alt_kategori,
                    'isvar':True,
                    'max_fiyat':max_fiyat,
                    
                }
                return render(request,"isler/isler.html",context)
            elif 'min_fiyat' in request.POST:
                min_fiyat =int(request.POST['min_fiyat'])
                is_max = İsBilgileri.objects.filter(kategori=kategori.id).order_by('fiyat').last()
                is_fiyat = İsBilgileri.objects.filter(kategori=kategori.id).filter(fiyat__range=(min_fiyat,is_max.fiyat))      
                context={
                    'is':is_fiyat,
                    'kategoriListe':kategori,
                    'altKategori':alt_kategori,
                    'isvar':True,
                    'min_fiyat':min_fiyat,
                    
                }
                return render(request,"isler/isler.html",context)

            elif 'max_fiyat' in request.POST and 'min_fiyat' in request.POST:
                      
                min_fiyat =int(request.POST['min_fiyat'])
                max_fiyat =int(request.POST['max_fiyat'])
                is_fiyat = İsBilgileri.objects.filter(kategori=kategori.id).filter(fiyat__range=(min_fiyat,max_fiyat))      
                context={
                'is':is_fiyat,
                'kategoriListe':kategori,
                'altKategori':alt_kategori,
                'isvar':True,
                'min_fiyat':min_fiyat,
                'max_fiyat':max_fiyat,
                
                }
                return render(request,"isler/isler.html",context)
            else:
                min_fiyat =int(request.POST['min_fiyat'])
                max_fiyat =int(request.POST['max_fiyat'])
                altkategori = request.POST['alt-kategori']
                altKategori = AltKategori.objects.get(altKategoriAd = altkategori)
                is_altkategori= İsBilgileri.objects.filter(alt_kategori = altKategori.id)
                is_filter=is_altkategori.filter(fiyat__range=(min_fiyat,max_fiyat))
                context={
                    'is':is_filter,
                    'kategoriListe':kategori,
                    'altKategori':alt_kategori,
                    'isvar':True,
                    'min_fiyat':min_fiyat,
                    'max_fiyat':max_fiyat,
                    
                }
                return render(request,"isler/isler.html",context)
        else:
            context={
                'is':is_filter,
                'kategoriListe':kategori,
                'altKategori':alt_kategori,
                'isvar':True,
                
                
            }
            return render(request,"isler/isler.html",context)
    else:
        context={
            'error':'İş Yok',
            'isvar':False,
            'kategoriListe':kategori,
            'altKategori':alt_kategori,


        }
        return render(request,"isler/isler.html",context)

  
def altkategori_view(request,slug):
    alt_kategori = AltKategori.objects.get(slug=slug)
    is_filter = İsBilgileri.objects.filter(alt_kategori=alt_kategori.id)
    kategori = Kategori.objects.get(id=alt_kategori.kategori.id)
    altkategori = AltKategori.objects.filter(kategori=kategori.id)
    if is_filter.exists():
        
        context={
            'is':is_filter,
            'kategoriListe':kategori,
            'altKategori':altkategori,
            'isvar':True,
            'selectedslug':slug,
        }
        return render(request,"isler/isler.html",context)
    else:
        context={
            'error':'İş Yok',
            'isvar':False,
            'kategoriListe':kategori,
            'altKategori':altkategori,
            'selectedslug':slug,
        }
        return render(request,"isler/isler.html",context)

def icerik_view(request):
    return render(request,'isler/isicerik.html')

def basvur_view(request):
    return render(request,'isler/basvur.html')