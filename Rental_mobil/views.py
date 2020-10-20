from django.shortcuts import render

from sewa_mobil.models import Testimoni

def index_view(request):
    
    testi = Testimoni.objects.all()[0:4]

    return render(request, 'main/index.html', {'testi':testi})

def contact_view(request):
    return render(request, 'main/contact.html')

def about_view(request):
    return render(request, 'main/about.html')


