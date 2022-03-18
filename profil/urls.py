from django.urls import path
from . import views
urlpatterns = [
    path('profilim/<str:username>',views.profil_view,name="profil"),
    path('hesap-ayarlari/<str:username>',views.hesapAyarlari_view,name="hesap-ayarlari")
]
