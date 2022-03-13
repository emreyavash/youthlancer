from unicodedata import name
from django.urls import path
from .views import kayit_ol,giris_yap
urlpatterns = [
    path('kayit-ol/',kayit_ol,name="kayit_ol"),
    path('giris-yap/',giris_yap,name="giris_yap")
]
