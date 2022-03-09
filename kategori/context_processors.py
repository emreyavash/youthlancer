from .models import Kategori,AltKategori

def kategori(request):
    
    kategori=Kategori.objects.all()
    return {'kategori':kategori}