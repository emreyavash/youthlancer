from django.urls import path
from . import views
urlpatterns = [
    path('',views.anasayfa_view,name="anasayfa"),
]
