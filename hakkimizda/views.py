from django.shortcuts import render

# Create your views here.

def hakkimizda_view(request):
    return render(request,'hakkimizda/about.html')