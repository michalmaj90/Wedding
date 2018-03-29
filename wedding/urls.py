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
from guests.views import HelloView, CoupleLoginView, GuestLoginView, GuestRegisterView, CouplePageView, CoupleLogoutView, GuestLogoutView, SpousePageView, SpouseAddInfoView, SpouseInfoView, SpouseEditInfoView, SpouseDeleteView, WeddingPageView, AddWeddingInfoView, WeddingInfoView, EditWeddingInfoView, WeddingDeleteView, GuestPageView, GuestInfoView, GuestAddInfoView, GuestDeleteInfoView, GuestEditInfoView, GuestCoupleInfoView, GuestWeddingInfoView, CoupleRegisterView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^hello/', HelloView.as_view(), name='hello'),
    url(r'^couple_login/', CoupleLoginView.as_view(), name='couple-login'),
    url(r'^couple_register', CoupleRegisterView.as_view(), name='couple-register'),
    url(r'^guest_login/', GuestLoginView.as_view(), name='guest-login'),
    url(r'^guest_register/', GuestRegisterView.as_view(), name='guest-register'),
    url(r'^couple_page', CouplePageView.as_view(), name='couple-page'),
    url(r'^couple_logut/', CoupleLogoutView.as_view(), name='couple-logout'),
    url(r'^guest_logout/', GuestLogoutView.as_view(), name='guest-logout'),
    url(r'^spouse_page', SpousePageView.as_view()),
    url(r'^spouse_add_info', SpouseAddInfoView.as_view(), name='spouse-add-info'),
    url(r'^spouse_info', SpouseInfoView.as_view(), name='spouse-info'),
    url(r'^spouse_edit_info/(?P<spouse_id>(\d)+)$', SpouseEditInfoView.as_view(), name='spouse-edit-info'),
    url(r'^spouse_delete/(?P<spouse_id>(\d)+)$', SpouseDeleteView.as_view(), name='spouse-delete'),
    url(r'^wedding_page/', WeddingPageView.as_view(), name='wedding-page'),
    url(r'^wedding_add_info', AddWeddingInfoView.as_view(), name='add-wedding-info'),
    url(r'^wedding_info', WeddingInfoView.as_view(), name='wedding-info'),
    url(r'^wedding_edit_info/(?P<wedding_id>(\d)+)$', EditWeddingInfoView.as_view(), name='wedding-edit-info'),
    url(r'^wedding_delete/(?P<wedding_id>(\d)+)$', WeddingDeleteView.as_view(), name='wedding-delete'),
    url(r'^guest_page/(?P<guest_id>(\d)+)$', GuestPageView.as_view(), name='guest-page'),
    url(r'^guest_info/(?P<guest_id>(\d)+)$', GuestInfoView.as_view(), name='guest-info'),
    url(r'^guest_add_info/(?P<guest_id>(\d)+)$', GuestAddInfoView.as_view(), name='guest-add-info'),
    url(r'^guest_delete_info/(?P<guest_id>(\d)+)$', GuestDeleteInfoView.as_view(), name='guest-delete-info'),
    url(r'^guest_edit_info/(?P<guest_id>(\d)+)$', GuestEditInfoView.as_view(), name='guest-edit-info'),
    url(r'^guest_couple_info', GuestCoupleInfoView.as_view(), name='guest-couple-info'),
    url(r'^guest_wedding_info', GuestWeddingInfoView.as_view(), name='guest-wedding-info')

]
