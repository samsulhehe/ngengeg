from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.models import User

import datetime

from sewa_mobil.models import Pesanan, Mobil
from .forms import UserForm

def register_view(request):

    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)

        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            user = authenticate(username=user_form.cleaned_data['username'],
                                password=user_form.cleaned_data['password'])
            registered = True
            login(request,user)
            return HttpResponseRedirect(reverse('home'))
        else:
            print(user_form.errors)
    else:
        user_form = UserForm()
    return render(request, 'accounts/register.html', {'form': user_form, 'registered':registered})


def login_view(request):

    q = request.GET.get("next")

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)

            if not q:

                return HttpResponseRedirect(reverse('home'))
            else:
                return HttpResponseRedirect(q)

        else:
            return HttpResponse('Invalid login details!')

    return render(request, 'accounts/login.html', {})
        

@login_required
def logout_view(request):
    logout(request)

    return HttpResponseRedirect(reverse('home'))


@login_required
def dashboard_view(request):
    pesanan = Pesanan.objects.filter(user=request.user)

    date_format = "%Y-%m-%d"
    
    i = 0
    
    if len(pesanan) > 0:
        for x in pesanan:
            
            pesan = datetime.datetime.strptime(str(pesanan[i].tgl_pesan), date_format)
            kembali = datetime.datetime.strptime(str(pesanan[i].tgl_kembali), date_format)

            hari = kembali - pesan
            i+=1

    q = request.GET.get("plat")

    if q:
        pesanan_ = get_object_or_404(Pesanan, mobil__plat=q)
        if request.user == pesanan_.user:
            mobil = get_object_or_404(Mobil, plat=q)
            mobil.status = "Available"
            mobil.save()
            pesanan_.delete()
            return HttpResponseRedirect(reverse("dashboard"))
        else:
            return HttpResponseForbidden()


    if len(pesanan) > 0:
        return render(request, 'accounts/dashboard.html', {'pesanan':pesanan, 'hari':hari.days})
    else:
        return render(request, 'accounts/dashboard.html')


