from tkinter.tix import MAX
from django.shortcuts import render
from kategori.models import Kategori,AltKategori
from isler.models import İsBilgileri
from django.db.models import Q
# Create your views here.
def filtering(param):
    return param != '' and param is not None

def isler_view(request,slug):

    kategori = Kategori.objects.get(slug=slug)
    is_filter = İsBilgileri.objects.filter(kategori=kategori.id)
    alt_kategori = AltKategori.objects.filter(kategori=kategori.id)

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
            }
            return render(request,"isler/isler.html",context)

        else:
            context={
                'error':'İş Yok',
                'kategoriListe':kategori,
                'altKategori':alt_kategori,
            }
            return render(request,"isler/isler.html",context)


    else:
        context={
            'error':'İş Yok',
            'kategoriListe':kategori,
            'altKategori':alt_kategori,


        }
        return render(request,"isler/isler.html",context)



def icerik_view(request):
    return render(request,'isler/isicerik.html')

def basvur_view(request):
    return render(request,'isler/basvur.html')