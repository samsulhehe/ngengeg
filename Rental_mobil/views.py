from django.shortcuts import render

def index_view(request):
    return render(request, 'main/index.html')

def contact_view(request):
    return render(request, 'main/contact.html')

def about_view(request):
    return render(request, 'main/about.html')


