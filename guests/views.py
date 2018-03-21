from django.shortcuts import render
from django.views import View
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from guests.models import WeddingCouple, WeddingGuest, AccompanyingPerson, WeddingInfo
from guests.forms import CoupleLoginForm, GuestLoginForm, GuestRegisterForm

# Create your views here.

class HelloView(View):
    def get(self, request):
        ctx = {}
        return render(request, 'hello.html', ctx)

class CoupleLoginView(View):
    def get(self, request):
        form = CoupleLoginForm()
        ctx = {
            'form': form,
        }
        return render(request, 'couple_login.html', ctx)

    def post(self, request):
        form = CoupleLoginForm(request.POST)
        if form.is_valid():
            user_aut = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user_aut is not None:
                user = User.objects.get(username=form.cleaned_data['username'])
                if user.is_superuser:
                    return HttpResponseRedirect("/couple_page")
                else:
                    return HttpResponse("Nie jesteś z pary młodej!")
            else:
                return HttpResponse("Taki użytkownik nie istnieje!")


class GuestLoginView(View):
    def get(self, request):
        form = GuestLoginForm()
        ctx = {
            'form': form,
        }
        return render(request, 'guest_login.html', ctx)

    def post(self, request):
        form = GuestLoginForm(request.POST)
        if form.is_valid():
            user_aut = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user_aut is not None:
                return HttpResponseRedirect('/guest_page/{}'.format(user_aut.id))
            else:
                ctx = {
                    'form': form,
                    'error': "Taki użytkownik nie istnieje!"
                }
                return render(request, 'guest_login.html', ctx)


class GuestRegisterView(View):
    def get(self, request):
        form = GuestRegisterForm()
        ctx = {
            'form': form,
        }
        return render(request, 'guest_register.html', ctx)

    def post(self, request):
        form = GuestRegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            user = User.objects.filter(username=username)
            password1 = form.cleaned_data['password1']
            password2 = form.cleaned_data['password2']
            if user:
                ctx = {
                    'form': form,
                    'error': "Podany użytkownik już istnieje!",
                }
                return render(request, 'guest_register.html', ctx)
            else:
                if password1 != password2:
                    ctx = {
                        'form': form,
                        'error': "Podane hasła są różne!",
                    }
                    return render(request, 'guest_register.html', ctx)
                else:
                    user = User.objects.create_user(username=username, password=password1)
                    return HttpResponseRedirect('/guest_page/{}'.format(user.id))
