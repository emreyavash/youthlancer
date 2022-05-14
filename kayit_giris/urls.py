from unicodedata import name
from django.urls import path,re_path
from . import views
urlpatterns = [
    re_path(r'^kayit-ol/$',views.kayit_ol,name="kayit_ol"),
    path('giris-yap/',views.giris_yap,name="giris_yap"),
    path('cikis/',views.cikis,name="cikis")
]
