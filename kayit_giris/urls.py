from unicodedata import name
from django.urls import path,re_path
from . import views
urlpatterns = [
    re_path(r'^kayit-ol/$',views.kayit_ol,name="kayit_ol"),
    path('giris-yap/',views.giris_yap,name="giris_yap"),
    path('cikis/',views.cikis,name="cikis"),
    path("email_dogrulama-user/<uidb64>/<token>",views.email_dogrulama,name="email_dogrulama"),
    path("sifre-degistirme-talebi/",views.sifre_degistirme_email,name="sifre_degistirme_email"),
    path("sifremi-unuttum/<uidb64>/<token>",views.sifre_degistirme_link,name="sifre_degistirme_link"),
     path("sifremi-unuttum/<username>",views.sifre_mi_unuttum,name="sifre_mi_unuttum"),
]
