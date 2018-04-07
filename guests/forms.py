from django import forms
from django.forms import ModelForm
from guests.models import FOOD
from guests.validators import validate_email

class CoupleLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class CoupleRegisterForm(forms.Form):
    username = forms.CharField()
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField(validators=[validate_email])

class GuestLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class GuestRegisterForm(forms.Form):
    username = forms.CharField()
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

class GuestAddInfoForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField(validators=[validate_email])
    phone = forms.IntegerField()
    food = forms.CharField(widget=forms.Select(choices=FOOD))

class SpouseAddInfoForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    description = forms.CharField(widget=forms.Textarea)
    email = forms.EmailField(validators=[validate_email])
    phone = forms.IntegerField()

class SpouseEditInfoForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    description = forms.CharField(widget=forms.Textarea)
    email = forms.EmailField(validators=[validate_email])
    phone = forms.IntegerField()

class AddWeddingInfoForm(forms.Form):
    church_name = forms.CharField()
    church_address = forms.CharField()
    church_view = forms.CharField(widget=forms.Textarea)
    premises_name = forms.CharField()
    premises_address = forms.CharField()
    premises_view = forms.CharField(widget=forms.Textarea)

class EditWeddingInfoForm(forms.Form):
    church_name = forms.CharField()
    church_address = forms.CharField()
    church_view = forms.CharField(widget=forms.Textarea)
    premises_name = forms.CharField()
    premises_address = forms.CharField()
    premises_view = forms.CharField(widget=forms.Textarea)

class GuestEditInfoForm(forms.Form):
    first_name = forms.CharField(initial='Imię')
    last_name = forms.CharField()
    email = forms.EmailField(validators=[validate_email])
    phone = forms.IntegerField()
    food = forms.CharField(widget=forms.Select(choices=FOOD))

class CompanionAddInfoForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    food = forms.CharField(widget=forms.Select(choices=FOOD))

class CompanionEditInfoForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    food = forms.CharField(widget=forms.Select(choices=FOOD))
