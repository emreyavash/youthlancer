from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
# Create your views here.

def kayit_ol(request):
    if request.user.is_authenticated:
        return redirect('anasayfa')
    if request.method == "POST":
        kullanici_adi = request.POST['kullanici_adi']
        isim = request.POST['isim']
        soyisim = request.POST['soyisim']
        email = request.POST['email']
        parola = request.POST['parola']
        parola2 = request.POST['parola2']
        if parola == parola2:
            if User.objects.filter(username = kullanici_adi).exists():
                context={
                    'error':"Kullanıcı Adı Kullanılıyor",
                    'isim':isim,
                    'soyisim':soyisim,
                    'email':email,
                    }
                return render(request,"kayit_giris/kayitol.html",context)
                
            elif User.objects.filter(email = email).exists():
                context={
                    'error':"Email Kullanılıyor",
                    'isim':isim,
                    'soyisim':soyisim,
                    'kullanici_adi':kullanici_adi,
                    }
                return render(request,"kayit_giris/kayitol.html",context)

            else:
                user = User.objects.create_user(username=kullanici_adi,first_name=isim,last_name=soyisim,email=email,password = parola)
                user.save()
                return redirect('anasayfa')

        else:
            context={
                'error':"Girdiğiniz Parolalar Eşleşmiyor",
                'kullanici_adi':kullanici_adi,
                'isim':isim,
                'soyisim':soyisim,
                'email':email,
                }
            return render(request,"kayit_giris/kayitol.html",context)
     
    else:
        return render(request,"kayit_giris/kayitol.html")
    

def giris_yap(request):
    if request.user.is_authenticated:
        return redirect('anasayfa')
    
    if request.method == "POST":
        kullanici_adi = request.POST['kullanici_adi']
        parola = request.POST['parola']

        user = authenticate(request,username = kullanici_adi,password = parola)

        if user is not None:
            if user.is_staff:
                login(request,user)
                return redirect('anasayfa')
            else:
                return render(request,"kayit_giris/girisyap.html",{
                "error":"Email is not verified,please check your email inbox",
                
                })  
        else:
             return render(request,"kayit_giris/girisyap.html",{
                "error":"Kullanıcı Adı veya Parola Yanlış",
                "user":user
            }) 

    return render(request,"kayit_giris/girisyap.html")

def cikis(request):
    logout(request)
    return redirect('anasayfa')
