from django.urls import path
from . import views
urlpatterns = [
    path('',views.ogrenci_dogrulama,name="ogrenci_dogrulama"),
    path('onayla/<str:username>/',views.onaylama,name="onayla"),
    path('sil/<str:username>/',views.sil,name="sil")
]

