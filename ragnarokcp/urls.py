"""
ragnarokcp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
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
from django.contrib import admin
from django.conf.urls import url, include

from unitedcp.views import *

urlpatterns = [
    # Admin URLs
    url(r'^admin/', admin.site.urls),

    # User URLs
    url(r'^$', main_page, name='/'),
    url(r'^promo/', home_page, name='promo'),
    url(r'^auth/login/', auth_login, name='auth_login'),
    url(r'^auth/register/', auth_register, name='auth_register'),
    url(r'^auth/logout/', auth_logout, name='auth_logout'),
    url(r'^auth/password/reset/', user_password_reset, name='user_password_reset'),
    url(r'^verify/(?P<key>.*)/(?P<action>.*)/', user_verification, name='user_verification'),

    # Accounts
    url(r'^account/', include('unitedcp.accounts.urls')),

    # News
    url(r'^article/(?P<article_id>.*)/', read_news, name='news_read'),

    # Ragnarok
    url(r'^game/', include('unitedcp.ragnarok.urls')),

    # Donations
    url(r'^donations/', include('unitedcp.donations.urls')),

    # Staff
    url(r'^staff/', include('unitedcp.staff.urls')),

    # Rankings
    url(r'^rankings/', include('unitedcp.rankings.urls')),

    # Addons
    url(r'^addon/', include('unitedcp.addons.urls')),

    # Guides
    url(r'^guides/', include('unitedcp.guides.urls')),
    # Testing
    # url(r'^system/tests/email/', test_email, name='test_email'),

    # Translation
    url(r'^i18n/', include('django.conf.urls.i18n')),

    # Shop
    url(r'^shop/', include('unitedcp.shop.urls')),
]
