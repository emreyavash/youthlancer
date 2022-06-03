from random import randint
from urllib.parse import urljoin
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect

from profil.models import Kullanici
from .models import ParaCekme,ParaYatirma,ToplamBakiye
from isler.models import Secilen_Freelancer
import base64
import hmac
import hashlib
import requests
import json

from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt
# Create your views here.


def para_yatirma(request,username,is_id):
    is_veren = User.objects.get(username = username)
    if request.user.username == username:
        biten_is = Secilen_Freelancer.objects.get(is_bilgi = is_id,is_veren= is_veren.id)
        if request.method == 'POST':
           
            kullanici = User.objects.get(username = username)
            kullanici_bilgileri = Kullanici.objects.get(user = kullanici.id)

            
            merchant_id = '213301'
            merchant_key = b'Bd2tjDxt74F7SXB5'
            merchant_salt = b'cDL8G6WXqMGSgS8W'
            # Müşterinizin sitenizde kayıtlı veya form vasıtasıyla aldığınız eposta adresi
            email = f'{kullanici.email}'

            # Tahsil edilecek tutar.
            fiyat = biten_is.is_bilgi.fiyat*100
            payment_amount = f'{fiyat}' # 9.99 için 9.99 * 100 = 999 gönderilmelidir.

            # Sipariş numarası: Her işlemde benzersiz olmalıdır!! Bu bilgi bildirim sayfanıza yapılacak bildirimde geri gönderilir.
            random1 = randint(1,999)
            random2 = randint(1,999)
            random3 = randint(1,999)
            merchant_oid = f'{100*random1*random2*random3}'

            # Müşterinizin sitenizde kayıtlı veya form aracılığıyla aldığınız ad ve soyad bilgisi
            isim_soyisim = f'{kullanici.first_name} {kullanici.last_name} '
            user_name =  isim_soyisim  

            # Müşterinizin sitenizde kayıtlı veya form aracılığıyla aldığınız adres bilgisi
            user_address = f'{kullanici_bilgileri.sehir.sehir}'

            # Müşterinizin sitenizde kayıtlı veya form aracılığıyla aldığınız telefon bilgisi
            user_phone = f'{kullanici_bilgileri.telefon}'

            # Başarılı ödeme sonrası müşterinizin yönlendirileceği sayfa
            # !!! Bu sayfa siparişi onaylayacağınız sayfa değildir! Yalnızca müşterinizi bilgilendireceğiniz sayfadır!
            # !!! Siparişi onaylayacağız sayfa "Bildirim URL" sayfasıdır (Bakınız: 2.ADIM Klasörü).
            merchant_ok_url ='http://www.siteniz.com/odeme_basarili.php'


            # Ödeme sürecinde beklenmedik bir hata oluşması durumunda müşterinizin yönlendirileceği sayfa
            # !!! Bu sayfa siparişi iptal edeceğiniz sayfa değildir! Yalnızca müşterinizi bilgilendireceğiniz sayfadır!
            # !!! Siparişi iptal edeceğiniz sayfa "Bildirim URL" sayfasıdır (Bakınız: 2.ADIM Klasörü).
            merchant_fail_url = 'http://www.siteniz.com/odeme_hata.php'
            # Müşterinin sepet/sipariş içeriği
            user_basket =  base64.b64encode(json.dumps([[f'{biten_is.is_bilgi.is_isim}', f'{biten_is.is_bilgi.fiyat}', 1],
                    ]).encode())

            # ÖRNEK $user_basket oluşturma - Ürün adedine göre array'leri çoğaltabilirsiniz
            """
            user_basket = base64.b64encode(json.dumps([['Örnek ürün 1', '18.00', 1],
                        ['Örnek ürün 2', '33.25', 2],
                        ['Örnek ürün 3', '45.42', 1]]).encode())
            """

            # !!! Eğer bu örnek kodu sunucuda değil local makinanızda çalıştırıyorsanız
            # buraya dış ip adresinizi (https://www.81.213.78.132.com/) yazmalısınız. Aksi halde geçersiz paytr_token hatası alırsınız.
            user_ip = '88.230.183.3'

            # İşlem zaman aşımı süresi - dakika cinsinden
            timeout_limit = '30'

            # Hata mesajlarının ekrana basılması için entegrasyon ve test sürecinde 1 olarak bırakın. Daha sonra 0 yapabilirsiniz.
            debug_on = '1'

            # Mağaza canlı modda iken test işlem yapmak için 1 olarak gönderilebilir.
            test_mode = '1'

            no_installment = '1' # Taksit yapılmasını istemiyorsanız, sadece tek çekim sunacaksanız 1 yapın

            # Sayfada görüntülenecek taksit adedini sınırlamak istiyorsanız uygun şekilde değiştirin.
            # Sıfır (0) gönderilmesi durumunda yürürlükteki en fazla izin verilen taksit geçerli olur.
            max_installment = '0'

            currency = 'TL'

            # Bu kısımda herhangi bir değişiklik yapmanıza gerek yoktur.
            hash_str = merchant_id + user_ip + merchant_oid + email + payment_amount + user_basket.decode() + no_installment + max_installment + currency + test_mode
            paytr_token = base64.b64encode(hmac.new(merchant_key, hash_str.encode() + merchant_salt, hashlib.sha256).digest())

            params = {
                'merchant_id': merchant_id,
                'user_ip': user_ip,
                'merchant_oid': merchant_oid,
                'email': email,
                'payment_amount': payment_amount,
                'paytr_token': paytr_token,
                'user_basket': user_basket,
                'debug_on': debug_on,
                'no_installment': no_installment,
                'max_installment': max_installment,
                'user_name': user_name,
                'user_address': user_address,
                'user_phone': user_phone,
                'merchant_ok_url': merchant_ok_url,
                'merchant_fail_url': merchant_fail_url,
                'timeout_limit': timeout_limit,
                'currency': currency,
                'test_mode': test_mode
            }

            result = requests.post('https://www.paytr.com/odeme/api/get-token', params)
            res = json.loads(result.text)

            if res['status'] == 'success':
                print(res['token'] )

                context = {
                    'token': res['token'],
                    
                }
                ParaYatirma.objects.create(isveren = biten_is.is_veren,freelancer= biten_is.user,yapilan_is = biten_is.is_bilgi,yatırılan_tutar=fiyat )
                return render(request,'para_islemleri/odeme_sayfasi.html',context)
                
            else:
                print(result.text)  
            
                context = {
                    
                    'deneme':'hata'
                }
                return render(request,'para_islemleri/odeme.html',context)
            
        context={
            'yapilan_is':biten_is,
            
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


# Bildirimler
@csrf_exempt
def callback(request):

    if request.method != 'POST':
        return HttpResponse(str(''))

    post = request.POST

    # API Entegrasyon Bilgileri - Mağaza paneline giriş yaparak BİLGİ sayfasından alabilirsiniz.
    merchant_key = b'YYYYYYYYYYYYYY'
    merchant_salt = 'ZZZZZZZZZZZZZZ'

    # Bu kısımda herhangi bir değişiklik yapmanıza gerek yoktur.
    # POST değerleri ile hash oluştur.
    hash_str = post['merchant_oid'] + merchant_salt + post['status'] + post['total_amount']
    hash = base64.b64encode(hmac.new(merchant_key, hash_str.encode(), hashlib.sha256).digest())

    # Oluşturulan hash'i, paytr'dan gelen post içindeki hash ile karşılaştır
    # (isteğin paytr'dan geldiğine ve değişmediğine emin olmak için)
    # Bu işlemi yapmazsanız maddi zarara uğramanız olasıdır.
    if hash != post['hash']:
        return HttpResponse(str('PAYTR notification failed: bad hash'))

    # BURADA YAPILMASI GEREKENLER
    # 1) Siparişin durumunu post['merchant_oid'] değerini kullanarak veri tabanınızdan sorgulayın.
    # 2) Eğer sipariş zaten daha önceden onaylandıysa veya iptal edildiyse "OK" yaparak sonlandırın.

    if post['status'] == 'success':  # Ödeme Onaylandı
        """
        BURADA YAPILMASI GEREKENLER
        1) Siparişi onaylayın.
        2) Eğer müşterinize mesaj / SMS / e-posta gibi bilgilendirme yapacaksanız bu aşamada yapmalısınız.
        3) 1. ADIM'da gönderilen payment_amount sipariş tutarı taksitli alışveriş yapılması durumunda değişebilir. 
        Güncel tutarı post['total_amount'] değerinden alarak muhasebe işlemlerinizde kullanabilirsiniz.
        """
        print(request)
    else:  # Ödemeye Onay Verilmedi
        """
        BURADA YAPILMASI GEREKENLER
        1) Siparişi iptal edin.
        2) Eğer ödemenin onaylanmama sebebini kayıt edecekseniz aşağıdaki değerleri kullanabilirsiniz.
        post['failed_reason_code'] - başarısız hata kodu
        post['failed_reason_msg'] - başarısız hata mesajı
        """
        print(request)

    # Bildirimin alındığını PayTR sistemine bildir.
    return HttpResponse(str('OK'))

