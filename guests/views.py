from django.shortcuts import render
from django.views import View
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from guests.models import WeddingCouple, WeddingGuest, AccompanyingPerson, WeddingInfo, FOOD
from guests.forms import CoupleLoginForm, GuestLoginForm, GuestRegisterForm, GuestAddInfoForm, SpouseAddInfoForm, SpouseEditInfoForm, AddWeddingInfoForm, EditWeddingInfoForm, GuestEditInfoForm

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
                    return HttpResponseRedirect("/couple_page")
                else:
                    ctx = {
                        'form': form,
                        'error': "Nie jesteś z pary młodej!"
                    }
                    return render(request, 'couple_login.html', ctx)
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
                    WeddingGuest.objects.create(user=user, first_name="", last_name="", email="", phone=None, food=None)
                    return HttpResponseRedirect('/guest_page/{}'.format(user.id))


class CouplePageView(View):
    def get(self, request):
        ctx = {}
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
    def get(self, request):
        spouse = WeddingCouple.objects.all()
        ctx = {
            'spouse': spouse,
            }
        return render(request, 'spouse_page.html', ctx)


class SpouseAddInfoView(View):
    def get(self, request):
        form = SpouseAddInfoForm()
        ctx = {
            'form': form,
        }
        return render(request, 'spouse_add_info.html', ctx)

    def post(self, request):
        form = SpouseAddInfoForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            description = form.cleaned_data['description']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            spouse = WeddingCouple.objects.create(first_name=first_name, last_name=last_name, description=description, email=email, phone=phone)
            return HttpResponseRedirect("/spouse_info/{}".format(spouse.id))


class SpouseInfoView(View):
    def get(self, request):
        spouses = WeddingCouple.objects.all()
        ctx = {
            'spouses': spouses,
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
            spouses = WeddingCouple.objects.all()
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
            ctx = {
                'text': "Zmieniono dane małżonka!",
                'spouses': spouses,
            }
            return render(request, 'spouse_info.html', ctx)


class SpouseDeleteView(View):
    def get(self, request, spouse_id):
        spouse = WeddingCouple.objects.get(pk=spouse_id)
        spouse.delete()
        return HttpResponseRedirect('/spouse_info')


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
            new_wedding = WeddingInfo.objects.create(church_name=church_name, church_address=church_address, church_view=church_view, premises_name=premises_name, premises_address=premises_address, premises_view=premises_view)
            infos = WeddingInfo.objects.all()
            ctx = {
                'infos': infos,
                'text': "Dodano informacje o weselu!",
            }
            return HttpResponseRedirect('/wedding_info')

class WeddingInfoView(View):
    def get(self, request):
        infos = WeddingInfo.objects.all()
        ctx = {
            'infos': infos,
        }
        return render(request, 'wedding_info.html', ctx)


class EditWeddingInfoView(View):
    def get(self, request, wedding_id):
        form = EditWeddingInfoForm()
        ctx = {
            'form': form,
        }
        return render(request, 'edit_wedding_info.html', ctx)

    def post(self, request, wedding_id):
        form = EditWeddingInfoForm(request.POST)
        if form.is_valid():
            info = WeddingInfo.objects.get(pk=wedding_id)
            church_name = form.cleaned_data['church_name']
            church_address = form.cleaned_data['church_address']
            church_view = form.cleaned_data['church_view']
            premises_name = form.cleaned_data['premises_name']
            premises_address = form.cleaned_data['premises_address']
            premises_view = form.cleaned_data['premises_view']
            if info.church_name != church_name:
                info.church_name = church_name
            if info.church_address != church_address:
                info.church_address = church_address
            if info.church_view != church_view:
                info.church_view = church_view
            if info.premises_name != premises_name:
                info.premises_name = premises_name
            if info.premises_address != premises_address:
                info.premises_address = premises_address
            if info.premises_view != premises_view:
                info.premises_view = premises_view
            info.save()
            return HttpResponseRedirect('/wedding_info')

class WeddingDeleteView(View):
    def get(self, request, wedding_id):
        wedding = WeddingInfo.objects.get(pk=wedding_id)
        wedding.delete()
        return HttpResponseRedirect('/wedding_info')


class GuestPageView(View):
    def get(self, request, guest_id):
        user = User.objects.get(pk=guest_id)
        guest = WeddingGuest.objects.get(user=user)
        ctx = {
            'guest': guest,
            'user': user,
        }
        return render(request, 'guest_page.html', ctx)

class GuestInfoView(View):
    def get(self, request, guest_id):
        user = User.objects.get(pk=guest_id)
        guest = WeddingGuest.objects.get(user=user)
        ctx = {
            'guest': guest,
            'user': user,
        }
        return render(request, 'guest_info.html', ctx)

class GuestAddInfoView(View):
    def get(self, request, guest_id):
        form = GuestAddInfoForm()
        ctx = {
            'form': form,
            'guest': guest_id,
        }
        return render(request, 'guest_add_info.html', ctx)

    def post(self, request, guest_id):
        form = GuestAddInfoForm(request.POST)
        user = User.objects.get(pk=guest_id)
        guest = WeddingGuest.objects.get(user=user)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            food = form.cleaned_data['food']
            guest.first_name = first_name
            guest.last_name = last_name
            guest.email = email
            guest.phone = phone
            guest.food = food
            guest.save()
            return HttpResponseRedirect('/guest_info/{}'.format(user.id))

class GuestDeleteInfoView(View):
    def get(self, request, guest_id):
        user = User.objects.get(pk=guest_id)
        guest = WeddingGuest.objects.get(user=user)
        guest.first_name = ""
        guest.last_name = ""
        guest.email = ""
        guest.phone = None
        guest.Food = None
        guest.save()
        return HttpResponseRedirect('/guest_info/{}'.format(guest_id))

class GuestEditInfoView(View):
    def get(self, request, guest_id):
        form = GuestEditInfoForm()
        user = User.objects.get(pk=guest_id)
        guest = WeddingGuest.objects.get(user=user)
        form.fields['first_name'].initial = guest.first_name
        form.fields['last_name'].initial = guest.last_name
        form.fields['email'].initial = guest.email
        form.fields['phone'].initial = guest.phone
        form.fields['food'].initial = guest.food
        ctx = {
            'form': form,
        }
        return render(request, 'guest_edit_info.html', ctx)

    def post(self, request, guest_id):
        form = GuestEditInfoForm(request.POST)
        if form.is_valid():
            user = User.objects.get(pk=guest_id)
            guest = WeddingGuest.objects.get(user=user)
            guest.first_name = form.cleaned_data['first_name']
            guest.last_name = form.cleaned_data['last_name']
            guest.email = form.cleaned_data['email']
            guest.phone = form.cleaned_data['phone']
            guest.food = form.cleaned_data['food']
            guest.save()
            return HttpResponseRedirect('/guest_info/{}'.format(user.id))
