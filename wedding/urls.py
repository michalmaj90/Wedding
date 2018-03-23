"""wedding URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from guests.views import HelloView, CoupleLoginView, GuestLoginView, GuestRegisterView, CouplePageView, CoupleLogoutView, GuestLogoutView, SpousePageView, SpouseAddInfoView, SpouseInfoView, SpouseEditInfoView, WeddingPageView, AddWeddingInfoView, WeddingInfoView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^hello/', HelloView.as_view(), name='hello'),
    url(r'^couple_login/', CoupleLoginView.as_view(), name='couple-login'),
    url(r'^guest_login/', GuestLoginView.as_view(), name='guest-login'),
    url(r'^guest_register/', GuestRegisterView.as_view(), name='guest-register'),
    url(r'^couple_page/(?P<spouse_id>(\d)+)$', CouplePageView.as_view(), name='couple-page'),
    url(r'^couple_logut/', CoupleLogoutView.as_view(), name='couple-logout'),
    url(r'^guest_logout/', GuestLogoutView.as_view(), name='guest-logout'),
    url(r'^spouse_page/(?P<spouse_id>(\d)+)$', SpousePageView.as_view()),
    url(r'^spouse_add_info/(?P<spouse_id>(\d)+)$', SpouseAddInfoView.as_view(), name='spouse-add-info'),
    url(r'^spouse_info/(?P<spouse_id>(\d)+)$', SpouseInfoView.as_view(), name='spouse-info'),
    url(r'^spouse_edit_info/(?P<spouse_id>(\d)+)$', SpouseEditInfoView.as_view(), name='spouse-edit-info'),
    url(r'^wedding_page/', WeddingPageView.as_view(), name='wedding-page'),
    url(r'^wedding_add_info', AddWeddingInfoView.as_view(), name='add-wedding-info'),
    url(r'^wedding_info/', WeddingInfoView.as_view(), name='wedding-info')

]
