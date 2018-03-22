from django import forms
from django.forms import ModelForm

class CoupleLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class GuestLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class GuestRegisterForm(forms.Form):
    username = forms.CharField()
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

class SpouseAddInfoForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    description = forms.CharField(widget=forms.Textarea)
    email = forms.CharField()
    phone = forms.IntegerField()
