from django.urls import path
from . import views
urlpatterns = [
    path('kategori/<slug:slug>',views.isler_view,name="isler"),
    path('<slug:slug>/',views.icerik_view,name="icerik"),
    path('basvur/<slug:slug>',views.basvur_view,name="basvur"),
    path('is-olustur/<str:username>',views.is_olustur,name="is_olustur"),
    path('onay/<int:is_id>,<int:user_id>',views.freelancer_onay,name='onayla'),
]
