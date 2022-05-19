from django.urls import path
from . import views
urlpatterns = [
    path('odeme/<str:username>/<int:is_id>',views.para_yatirma,name="odeme"),  
    path('para-cekme/<str:username>',views.para_cekme,name="para_cekme")   
]
