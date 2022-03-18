from django.shortcuts import render

# Create your views here.

def profil_view(request,username):

    return render(request,'profil/profil.html')

def hesapAyarlari_view(request,username):
    
    return render(request,'profil/hesapayarlari.html')