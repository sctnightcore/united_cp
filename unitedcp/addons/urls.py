from django.conf.urls import url, include

urlpatterns = [
    url(r'^vending/', include('unitedcp.addons.vending.urls')),
    url(r'^announcements/', include('unitedcp.addons.announcements.urls')),
]
