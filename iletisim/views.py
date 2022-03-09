from django.shortcuts import render

# Create your views here.
def iletisim_view(request):
    return render(request,"iletisim/iletisim.html")