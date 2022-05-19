from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.utils.encoding import force_bytes,force_str,DjangoUnicodeDecodeError
from django.core.mail import EmailMessage,send_mail

from profil.models import Kullanici
from .utils import generate_token
from django.conf import settings
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
            elif  request.POST.get('isveren_freelancer') is None:
                context={
                    'error':"Freelancer veya İşveren seçimi yapmalısın",
                    'isim':isim,
                    'soyisim':soyisim,
                    'kullanici_adi':kullanici_adi,
                    }
                return render(request,"kayit_giris/kayitol.html",context)
            else:
                if request.POST['isveren_freelancer'] == 'freelancer':
                    freelancer = True
                    isveren = False
                elif request.POST['isveren_freelancer'] == 'isveren':
                    isveren = True
                    freelancer = False
                user = User.objects.create_user(username=kullanici_adi,first_name=isim,last_name=soyisim,email=email,password = parola)
                user.save()
                kullanici = Kullanici.objects.create(user = user,freelancer= freelancer,isveren = isveren,kullanici_profil = False)
                kullanici.save()
                current_site=get_current_site(request)
                send_mail(
                    'Email Doğrulama',
                    render_to_string("kayit_giris/email_dogrulama.html",{
                        "user":user, 
                        "domain":current_site,
                        "uid":urlsafe_base64_encode(force_bytes(user.id)),
                        "token":generate_token.make_token(user)
                    }),
                    settings.DEFAULT_FROM_EMAIL,
                    [user.email],
                    fail_silently=False,
                )
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


def email_dogrulama(request,uidb64,token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(id=uid)
        token=generate_token.make_token(user)
    except Exception as e:
        user=None
    if user and generate_token.check_token(user,token):
        user.is_active=True
        user.is_staff=True
        user.save()

        return redirect("giris_yap")
    return render(request,"kayit_giris/email_dogrulama_hata.html",{
        "user":user
    })

def sifre_degistirme_email(request):
    if request.method == "POST":
        email = request.POST["email"]
        user = User.objects.get(email=email)
        if user.email==email:
            current_site=get_current_site(request)
            send_mail(
                'Parola Değişiliği',
                render_to_string("kayit_giris/sifre_degistirme_link.html",{
                    "user":user, 
                    "domain":current_site,
                    "uid":urlsafe_base64_encode(force_bytes(user.id)),
                    "token":generate_token.make_token(user)
                }),
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )
            return redirect("anasayfa")
        else:
            return render(request,"kayit_giris/sifre_mi_unuttum_email.html",{
                "error":"Email is wrong"
            })
    return render(request,"kayit_giris/sifre_mi_unuttum_email.html")

def sifre_degistirme_link(request,uidb64,token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(id=uid)
        token=generate_token.make_token(user)
    except Exception as e:
        user=None
    if user and generate_token.check_token(user,token):
        username = user.username
        return redirect("sifre_mi_unuttum",username=username)
    return render(request,"kayit_giris/sifre_mi_unuttum_email.html")

def sifre_mi_unuttum(request,username):
    if request.method == "POST":
        password = request.POST["password"]
        repassword = request.POST["repassword"]
        if password == repassword:
            user = User.objects.get(username=username)
            user.set_password(password)
            user.save()
            return redirect("giris_yap")
        else:
            return render(request,"kayit_giris/sifre_mi_unuttum.html",{
                "error":"Password doesn't match"
            })
    return render(request,"kayit_giris/sifre_mi_unuttum.html")
