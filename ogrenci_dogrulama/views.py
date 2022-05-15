from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from .models import OgrenciDogrulama
# Create your views here.
def dogrulama(file,username):
    ogrenci_user = User.objects.get(username = username)
    OgrenciDogrulama.objects.create(ogrenci_belge = file,kullanici = ogrenci_user)

def ogrenci_dogrulama(request):
    user = User.objects.get(id = request.user.id)  
    if user.is_superuser:
        gonderen_ogrenciler = OgrenciDogrulama.objects.all()
        context = {
            "gonderen_ogrenciler":gonderen_ogrenciler
        }
        return render(request,'ogrenci_dogrulama/ogrenci_list.html',context)
    else:
        return redirect('anasayfa')

def onaylama(request,username):
    ogrenci_user = User.objects.get(username = username)
    ogrenci_belge = OgrenciDogrulama.objects.get(kullanici = ogrenci_user)
    ogrenci_belge.is_correct = True
    ogrenci_belge.save()
    return redirect('ogrenci_dogrulama')

def sil(request,username):
    ogrenci_user = User.objects.get(username = username)
    ogrenci_belge = OgrenciDogrulama.objects.get(kullanici = ogrenci_user).delete()
    return redirect('ogrenci_dogrulama')
    