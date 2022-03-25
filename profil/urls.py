from unicodedata import name
from django.urls import path
from . import views
urlpatterns = [
    path('profilim/<str:username>',views.profil_view,
    name="profil"),
    path('hesap-ayarlari/<str:username>',views.hesapAyarlari_view,name="hesap-ayarlari"),
    path('profilim/yetenek-ekle/<str:username>',views.yetenek_ekle,name="yetenekEkle"),
    path('yetenek/<str:username>/<int:id>',views.yetenek_sil,name="yetenek_sil"),
    path('profilim/portfoy-ekle/<str:username>',views.portfoy_ekle,name="portfoyEkle"),
    path('portfolyo/<str:username>/<int:id>',views.portfoy_sil,name="portfoy_sil"),
    path('profilim/fotograf-ekle/<str:username>',views.fotograf_ekle,name="fotografEkle"),
    path('fotograf/<str:username>/<int:id>',views.fotograf_sil,name="fotograf_sil")
]
