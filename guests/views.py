from django.shortcuts import render
from django.views import View
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from guests.models import WeddingCouple, WeddingGuest, AccompanyingPerson, WeddingInfo
from guests.forms import CoupleLoginForm, GuestLoginForm, GuestRegisterForm, SpouseAddInfoForm, SpouseEditInfoForm, AddWeddingInfoForm

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
                    login(request, user)
                    return HttpResponseRedirect("/couple_page/{}".format(user.id))
                else:
                    return HttpResponse("Nie jesteś z pary młodej!")
            else:
                ctx = {
                    'form': form,
                    'error': "Taki użytkownik nie istnieje!"
                }
                return render(request, 'couple_login.html', ctx)

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
                login(request, user_aut)
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
                    login(request, user)
                    return HttpResponseRedirect('/guest_page/{}'.format(user.id))


class CouplePageView(View):
    def get(self, request, spouse_id):
        user = User.objects.get(pk=spouse_id)
        ctx = {
            'user': user,
        }
        return render(request, 'couple_page.html', ctx)

class CoupleLogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect('/couple_login')


class GuestLogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect('/guest_login')


class SpousePageView(View):
    def get(self, request, spouse_id):
        user = User.objects.get(pk=spouse_id)
        spouse = WeddingCouple.objects.filter(user=user)
        ctx = {
            'user': user,
            'spouse': spouse,
            }
        return render(request, 'spouse_page.html', ctx)


class SpouseAddInfoView(View):
    def get(self, request, spouse_id):
        form = SpouseAddInfoForm()
        ctx = {
            'form': form,
        }
        return render(request, 'spouse_add_info.html', ctx)

    def post(self, request, spouse_id):
        form = SpouseAddInfoForm(request.POST)
        if form.is_valid():
            user = User.objects.get(pk=spouse_id)
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            description = form.cleaned_data['description']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            spouse = WeddingCouple.objects.create(user=user, first_name=first_name, last_name=last_name, description=description, email=email, phone=phone)
            return HttpResponse("Witaj {}!".format(spouse.user))


class SpouseInfoView(View):
    def get(self, request, spouse_id):
        spouse = WeddingCouple.objects.get(pk=spouse_id)
        ctx = {
            'spouse': spouse,
        }
        return render(request, 'spouse_info.html', ctx)

class SpouseEditInfoView(View):
    def get(self, request, spouse_id):
        spouse = WeddingCouple.objects.get(pk=spouse_id)
        form = SpouseEditInfoForm()
        ctx = {
            'form': form,
        }
        return render(request, 'spouse_edit_info.html', ctx)

    def post(self, request, spouse_id):
        form = SpouseEditInfoForm(request.POST)
        if form.is_valid():
            spouse = WeddingCouple.objects.get(pk=spouse_id)
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            description = form.cleaned_data['description']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            if spouse.first_name != first_name:
                spouse.first_name = first_name
            if spouse.last_name != last_name:
                spouse.last_name = last_name
            if spouse.description != description:
                spouse.description = description
            if spouse.email != email:
                spouse.email = email
            if spouse.phone != phone:
                spouse.phone = phone
            spouse.save()
            return HttpResponseRedirect('/spouse_info/{}'.format(spouse_id))


class WeddingPageView(View):
    def get(self, request):
        infos = WeddingInfo.objects.all()
        ctx = {
            'infos': infos,
        }
        return render(request, 'wedding_page.html', ctx)


class AddWeddingInfoView(View):
    def get(self, request):
        form = AddWeddingInfoForm()
        ctx = {
            'form': form,
        }
        return render(request, 'add_wedding_info.html', ctx)

    def post(self, request):
        form = AddWeddingInfoForm(request.POST)
        if form.is_valid():
            church_name = form.cleaned_data['church_name']
            church_address = form.cleaned_data['church_address']
            church_view = form.cleaned_data['church_view']
            premises_name = form.cleaned_data['premises_name']
            premises_address = form.cleaned_data['premises_address']
            premises_view = form.cleaned_data['premises_view']
            WeddingInfo.objects.create(church_name=church_name, church_address=church_address, church_view=church_view, premises_name=premises_name, premises_address=premises_address, premises_view=premises_view)
            ctx = {
                'info': "Dodano informacje o weselu!"
            }
            return render(request, 'wedding_page.html', ctx)

class WeddingInfoView(View):
    def get(self, request):
        infos = WeddingInfo.objects.all()
        ctx = {
            'infos': infos,
        }
        return render(request, 'wedding_info.html', ctx)
