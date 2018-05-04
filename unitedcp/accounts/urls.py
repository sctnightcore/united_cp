from .views import *
from django.conf.urls import url

urlpatterns = [
    url(r'^dashboard/', control_panel, name='system_panel'),
    url(r'^me/', user_profile, name='user_profile'),
    url(r'^change/password/', user_change_password, name='user_change_password'),
    url(r'^change/email/', user_change_email, name='user_change_email'),
	url(r'^promo/', promo_page, name='promo_page'),
]
