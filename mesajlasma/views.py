from django.dispatch import receiver
from django.shortcuts import render
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist

from profil.models import Kullanici
from .models import Mesaj,MesajKanali

# Create your views here.

@login_required(login_url='giris_yap')
def mesajlar(request,username):
    user1 = User.objects.get(username = request.user.username)
    user = Kullanici.objects.get(user = user1.id)
    mesaj_atanlar = MesajKanali.objects.filter(Q(receiver_user = user.id) |Q(sender_user = user.id))

    
    
    context = {
        'mesaj_atanlar':mesaj_atanlar,
        'user':user
    }
    return render(request,'mesajlasma/mesajlar.html',context)

@login_required(login_url='giris_yap')
def mesajlasma(request,username):
    other_user = User.objects.get(username = username)
    other_user = Kullanici.objects.get(user = other_user.id)
    user = User.objects.get(username = request.user.username)

    if request.user.id > other_user.user.id:
        kanal = f'mesajlar_{user.id}-{other_user.user.id}'
    else:
        kanal = f'mesajlar_{other_user.user.id}-{user.id}'

    mesajlar = Mesaj.objects.filter(room = kanal)[0:25]
    context={
        'other_user':other_user,
        'user':user,
        'mesajlar':mesajlar,
        'kanal':kanal
    }
   
    return render(request,'mesajlasma/mesajkutusu.html',context)