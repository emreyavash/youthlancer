from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from .models import ParaCekme,ParaYatirma,ToplamBakiye
from isler.models import Secilen_Freelancer

# Create your views here.

def para_yatirma(request,username,is_id):
    is_veren = User.objects.get(username = username)
    if request.user.username == username:
        biten_is = Secilen_Freelancer.objects.get(is_bilgi = is_id,is_veren= is_veren.id)
        if request.method == 'POST':
            fiyat = request.POST.get('fiyat')
            print(fiyat)
            ParaYatirma.objects.create(isveren = biten_is.is_veren,freelancer= biten_is.user,yapilan_is = biten_is.is_bilgi,yatırılan_tutar=fiyat )
            return redirect('biten_isler',biten_is.is_veren.username)
        context={
            'yapilan_is':biten_is
        }
        return render(request,'para_islemleri/odeme.html',context)
    else:
        return redirect('anasayfa')

def para_cekme(request,username):
    freelancer = User.objects.get(username = username)
    if request.user.username == username:
        para_ceken = ToplamBakiye.objects.get(user = freelancer)
        if request.method == 'POST':
            if  request.POST.get('iban') == "":
                context={
                    'error':'iban girmek zorundasın'
                }
                return render(request,'para_islemleri/para_cekme.html',context)
            else:
                iban = request.POST['iban']

            tutar = request.POST['tutar']

            if int(tutar) > int(para_ceken.toplam_bakiye):
                context={
                    'error':'Bakiyenden fazlasını çekemezsin.'
                }
                return render(request,'para_islemleri/para_cekme.html',context)
            elif int(tutar)<0:
                context={
                    'error':'Negatif değer giremezsin.'
                }
                return render(request,'para_islemleri/para_cekme.html',context)
            
            cekilen_para=ParaCekme.objects.create(cekilen_tutar = tutar,iban = iban,user= freelancer)
            toplam_bakiye = int(para_ceken.toplam_bakiye)- int(cekilen_para.cekilen_tutar)
            toplam_cekilen_para =int(para_ceken.cekilen_para) + int(cekilen_para.cekilen_tutar)
            para_ceken.toplam_bakiye = toplam_bakiye
            para_ceken.cekilen_para = toplam_cekilen_para
            para_ceken.save()
            return redirect('hesap_ozeti',freelancer.username)
        else:
            return  render(request,'para_islemleri/para_cekme.html')
    else:
        return redirect('anasayfa')   