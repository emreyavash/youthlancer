from django.urls import path,re_path
from . import views
urlpatterns = [
    path('mesaj/<str:username>/',views.mesajlasma,name="mesajlasma"),
    path('mesajlar/<str:username>/',views.mesajlar,name="mesajlar")
]
