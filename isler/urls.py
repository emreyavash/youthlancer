from unicodedata import name
from django.urls import path,re_path
from . import views
urlpatterns = [
    path('kategori/<slug:slug>',views.isler_view,name="isler"),
    path('alt-kategori/<slug:slug>',views.altkategori_view,name="altisler"),
    path('web-sistesi-yaptırmak-istiyorum/',views.icerik_view,name="icerik"),
    path('basvur/',views.basvur_view,name="basvur")
]