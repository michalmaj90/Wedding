from django.shortcuts import render
from django.views import View
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.conf import settings
from guests.models import WeddingCouple, WeddingGuest, AccompanyingPerson, WeddingInfo, FOOD
from guests.forms import CoupleLoginForm, GuestLoginForm, GuestRegisterForm, GuestAddInfoForm, SpouseAddInfoForm, SpouseEditInfoForm, AddWeddingInfoForm, EditWeddingInfoForm, GuestEditInfoForm, CoupleRegisterForm, CompanionAddInfoForm, CompanionEditInfoForm

# Create your views here.

class HelloView(View):
    def get(self, request):
        ctx = {}
        return render(request, 'hello.html', ctx)

class CoupleRegisterView(View):
    def get(self, request):
        form = CoupleRegisterForm()
        ctx = {
            'form': form,
        }
        return render(request, 'couple_register.html', ctx)

    def post(self, request):
        form = CoupleRegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            user = User.objects.filter(username=username)
            password1 = form.cleaned_data['password1']
            password2 = form.cleaned_data['password2']
            email = form.cleaned_data['email']
            if user:
                ctx = {
                    'form': form,
                    'error': "Podany użytkownik już ustnieje!",
                }
                return render(request, 'couple_register.html', ctx)
            else:
                if password1 != password2:
                    ctx = {
                        'form': form,
                        'error': "Podane hasła są różne!",
                    }
                    return render(request, 'couple_register.html', ctx)
                else:
                    user = User.objects.create_superuser(username=username, password=password1, email=email)
                    login(request, user)
                    spouse = WeddingCouple.objects.create(user=user, first_name="", last_name="", description="", email="", phone=None)
                    return HttpResponseRedirect('/couple_page')
        else:
            ctx = {
                'form': form,
            }
            return render(request, 'couple_register.html', ctx)

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
            email = form.cleaned_data['email']
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
                    user = User.objects.create_user(username=username, password=password1, email=email)
                    login(request, user)
                    new_guest = WeddingGuest.objects.create(user=user, first_name="", last_name="", email="", phone=None, food=None)
                    AccompanyingPerson.objects.create(companion=new_guest, first_name="", last_name="", food="")
                    #send_mail(subject, message, from_email, to_email, fail_silently=True)
                    return HttpResponseRedirect('/guest_page/{}'.format(user.id))
        else:
            ctx = {
                'form': form,
            }
            return render(request, 'guest_register.html', ctx)


class CouplePageView(View):
    def get(self, request):
        ctx = {}
        return render(request, 'couple_page.html', ctx)

class CoupleInfoView(View):
    def get(self, request):
        spouses = WeddingCouple.objects.all()
        ctx = {
            'spouses': spouses,
        }
        return render(request, 'couple_info.html', ctx)

class CoupleLogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect('/couple_login')


class GuestLogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect('/guest_login')

class SpouseAddInfoView(View):
    def get(self, request, spouse_id):
        form = SpouseAddInfoForm()
        ctx = {
            'form': form,
            'spouse_id': spouse_id,
        }
        return render(request, 'spouse_add_info.html', ctx)

    def post(self, request, spouse_id):
        form = SpouseAddInfoForm(request.POST)
        if form.is_valid():
            user = User.objects.get(pk=spouse_id)
            spouse = WeddingCouple.objects.get(user=user)
            spouse.first_name = form.cleaned_data['first_name']
            spouse.last_name = form.cleaned_data['last_name']
            spouse.description = form.cleaned_data['description']
            spouse.email = form.cleaned_data['email']
            spouse.phone = form.cleaned_data['phone']
            spouse.save()
            return HttpResponseRedirect("/spouse_info/{}".format(spouse_id))
        else:
            ctx = {
                'form': form,
            }
            return render(request, 'spouse_add_info.html', ctx)


class SpouseInfoView(View):
    def get(self, request, spouse_id):
        user = User.objects.get(pk=spouse_id)
        spouse= WeddingCouple.objects.get(user=user)
        ctx = {
            'spouse': spouse,
        }
        return render(request, 'spouse_info.html', ctx)

class SpouseEditInfoView(View):
    def get(self, request, spouse_id):
        user = User.objects.get(pk=spouse_id)
        spouse = WeddingCouple.objects.get(user=user)
        form = SpouseEditInfoForm()
        form.fields['first_name'].initial = spouse.first_name
        form.fields['last_name'].initial = spouse.last_name
        form.fields['description'].initial = spouse.description
        form.fields['email'].initial = spouse.email
        form.fields['phone'].initial = spouse.phone
        ctx = {
            'form': form,
        }
        return render(request, 'spouse_edit_info.html', ctx)

    def post(self, request, spouse_id):
        form = SpouseEditInfoForm(request.POST)
        if form.is_valid():
            user = User.objects.get(pk=spouse_id)
            spouse = WeddingCouple.objects.get(user=user)
            spouse.first_name = form.cleaned_data['first_name']
            spouse.last_name = form.cleaned_data['last_name']
            spouse.description = form.cleaned_data['description']
            spouse.email = form.cleaned_data['email']
            spouse.phone = form.cleaned_data['phone']
            spouse.save()
            ctx = {
                'text': "Zmieniono dane małżonka!",
                'spouse': spouse,
            }
            return render(request, 'spouse_info.html', ctx)
        else:
            ctx = {
                'form': form,
            }
            return render(request, 'spouse_edit_info.html', ctx)


class SpouseDeleteView(View):
    def get(self, request, spouse_id):
        user = User.objects.get(pk=spouse_id)
        spouse = WeddingCouple.objects.get(user=user)
        spouse.first_name = ""
        spouse.last_name = ""
        spouse.description = ""
        spouse.email = ""
        spouse.phone = None
        spouse.save()
        return HttpResponseRedirect('/spouse_info/{}'.format(spouse_id))

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
        wedding = WeddingInfo.objects.get(pk=wedding_id)
        form.fields['church_name'].initial = wedding.church_name
        form.fields['church_address'].initial = wedding.church_address
        form.fields['church_view'].initial = wedding.church_view
        form.fields['premises_name'].initial = wedding.premises_name
        form.fields['premises_address'].initial = wedding.premises_address
        form.fields['premises_view'].initial = wedding.premises_view
        ctx = {
            'form': form,
        }
        return render(request, 'edit_wedding_info.html', ctx)

    def post(self, request, wedding_id):
        form = EditWeddingInfoForm(request.POST)
        if form.is_valid():
            info = WeddingInfo.objects.get(pk=wedding_id)
            info.church_name = form.cleaned_data['church_name']
            info.church_address = form.cleaned_data['church_address']
            info.church_view = form.cleaned_data['church_view']
            info.premises_name = form.cleaned_data['premises_name']
            info.premises_address = form.cleaned_data['premises_address']
            info.premises_view = form.cleaned_data['premises_view']
            info.save()
            return HttpResponseRedirect('/wedding_info')

class WeddingGuestsView(View):
    def get(self, request):
        guests = WeddingGuest.objects.all()
        companions = AccompanyingPerson.objects.all()
        empty_companions = AccompanyingPerson.objects.filter(first_name="")
        guests_number = len(guests) + (len(companions)-len(empty_companions))
        ctx = {
            'guests': guests,
            'companions': companions,
            'guests_number': guests_number,
        }
        return render(request, 'wedding_guests.html', ctx)

class WeddingGuestInfoView(View):
    def get(self, request, guest_id):
        user = User.objects.get(pk=guest_id)
        guest = WeddingGuest.objects.get(user=user)
        companion = AccompanyingPerson.objects.get(companion=guest)
        ctx = {
            'guest': guest,
            'companion': companion,
        }
        return render(request, 'wedding_guest_info.html', ctx)


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
        companion = AccompanyingPerson.objects.get(companion=guest)
        ctx = {
            'guest': guest,
            'user': user,
            'companion': companion,
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
        else:
            ctx = {
                'form': form,
            }
            return render(request, 'guest_add_info.html', ctx)

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
        else:
            ctx = {
                'form': form,
            }
            return render(request, 'guest_edit_info.html', ctx)


class CompanionInfoView(View):
    def get(self, request, companion_id):
        guest = WeddingGuest.objects.get(pk=companion_id)
        companion = AccompanyingPerson.objects.get(companion=guest)
        ctx = {
            'guest': guest,
            'companion': companion,
        }
        return render(request, 'companion_info.html', ctx)

class CompanionAddInfoView(View):
    def get(self, request, companion_id):
        form = CompanionAddInfoForm()
        guest = WeddingGuest.objects.get(pk=companion_id)
        companion = AccompanyingPerson.objects.get(companion=guest)
        ctx = {
            'form': form,
        }
        return render(request, 'companion_add_info.html', ctx)

    def post(self, request, companion_id):
        form = CompanionAddInfoForm(request.POST)
        if form.is_valid():
            guest = WeddingGuest.objects.get(pk=companion_id)
            companion = AccompanyingPerson.objects.get(companion=guest)
            companion.first_name = form.cleaned_data['first_name']
            companion.last_name = form.cleaned_data['last_name']
            companion.food = form.cleaned_data['food']
            companion.save()
            return HttpResponseRedirect('/companion_info/{}'.format(companion_id))

class CompanionEditInfoView(View):
    def get(self, request, companion_id):
        form = CompanionEditInfoForm()
        guest = WeddingGuest.objects.get(pk=companion_id)
        companion = AccompanyingPerson.objects.get(companion=guest)
        form.fields['first_name'].initial = companion.first_name
        form.fields['last_name'].initial = companion.last_name
        form.fields['food'].initial = companion.food
        ctx = {
            'form': form,
        }
        return render(request, 'companion_edit_info.html', ctx)

    def post(self, request, companion_id):
        form = CompanionEditInfoForm(request.POST)
        if form.is_valid():
            guest = WeddingGuest.objects.get(pk=companion_id)
            companion = AccompanyingPerson.objects.get(companion=guest)
            companion.first_name = form.cleaned_data['first_name']
            companion.last_name = form.cleaned_data['last_name']
            companion.food = form.cleaned_data['food']
            companion.save()
            return HttpResponseRedirect('/companion_info/{}'.format(companion_id))

class WeddingCompanionInfoView(View):
    def get(self, request, companion_id):
        guest = WeddingGuest.objects.get(pk=companion_id)
        companion = AccompanyingPerson.objects.get(companion=guest)
        ctx = {
            'companion': companion,
        }
        return render(request, 'wedding_companion_info.html', ctx)

class CompanionDeleteInfoView(View):
    def get(self, request, companion_id):
        guest = WeddingGuest.objects.get(pk=companion_id)
        companion = AccompanyingPerson.objects.get(companion=guest)
        companion.first_name = ""
        companion.last_name = ""
        companion.food = ""
        companion.save()
        return HttpResponseRedirect('/companion_info/{}'.format(companion_id))

class GuestCoupleInfoView(View):
    def get(self, request):
        couple = WeddingCouple.objects.all()
        ctx = {
            'couple': couple,
        }
        return render(request, 'guest_couple_info.html', ctx)

class GuestWeddingInfoView(View):
    def get(self, request):
        wedding = WeddingInfo.objects.all()
        ctx = {
            'wedding': wedding,
        }
        return render(request, 'guest_wedding_info.html', ctx)
