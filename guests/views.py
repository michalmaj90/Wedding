from django.shortcuts import render
from django.views import View
from guests.models import WeddingCouple, WeddingGuest, AccompanyingPerson, WeddingInfo

# Create your views here.

class HelloView(View):
    def get(self, request):
        ctx = {}
        return render(request, 'base.html', ctx)
