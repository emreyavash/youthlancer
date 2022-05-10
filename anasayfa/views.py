from django.shortcuts import render
# Create your views here.


def anasayfa_view(request):
    return render(request,"anasayfa/icerik.html")

