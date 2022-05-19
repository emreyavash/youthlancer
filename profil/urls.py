from django.urls import path
from . import views
urlpatterns = [
    path('profil/<str:username>',views.profil_view,
    name="profil"),
    path('hesap-ayarlari/<str:username>',views.hesapAyarlari_view,name="hesap-ayarlari"),
    path('profilim/yetenek-ekle/<str:username>',views.yetenek_ekle,name="yetenekEkle"),
    path('yetenek/<str:username>/<int:id>',views.yetenek_sil,name="yetenek_sil"),
    path('profilim/portfoy-ekle/<str:username>',views.portfoy_ekle,name="portfoyEkle"),
    path('portfolyo/<str:username>/<int:id>',views.portfoy_sil,name="portfoy_sil"),
    path('profilim/fotograf-ekle/<str:username>',views.fotograf_ekle,name="fotografEkle"),
    path('fotograf/<str:username>/<int:id>',views.fotograf_sil,name="fotograf_sil"),
    path('basvurulan-isler/<str:username>',views.basvurulan_isler,name='basvurulan_isler'),
    path('aldigin-isler/<str:username>',views.aldigin_isler,name='aldigin_isler'),
    path('basvuru_sil/<int:id>/<str:username>',views.basvuru_sil,name='basvuru_sil'),
    path('paylasilan-isler/<str:username>',views.paylasilan_isler,name='paylasilan_isler'),
    path('paylasilan-is-duzenle/<str:username>/<int:id>',views.is_duzenle,name='is_duzenle'),
    path('paylasilan_sil/<int:id>/<str:username>',views.paylasilan_sil,name='paylasilan_sil'),
    path('biten-isler/<str:username>',views.biten_isler,name='biten_isler'),
    path('kabul_edilen_freelancerlar/<str:username>',views.kabul_edilen_freelancerlar,name='kabul_edilen_freelancerlar'),
    path('kabul_edilen_freelancer_iptal/<int:is_id>/<int:id>',views.kabul_edilen_freelancer_iptal,name='kabul_edilen_freelancer_iptal'),
    path('kabul_edilen_freelancer_onay/<int:is_id>,<int:user_id>',views.kabul_edilen_freelancer_onay,name='kabul_edilen_freelancer_onay'),
    path('basvuran-freelancerlar/<str:username>',views.basvuran_freelancerlar,name='basvuran_freelancerlar'),
    path('onay/<int:is_id>,<int:user_id>',views.basvuran_freelancer_onay,name='onayla'),
    path('iptal/<int:is_id>,<int:user_id>',views.basvuran_freelancer_iptal,name='iptal'),
    path('hesap-ozeti/<str:username>',views.hesap_ozeti,name='hesap_ozeti'),



]
