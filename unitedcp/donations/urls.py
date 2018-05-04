from django.conf.urls import url
from .views import *


urlpatterns = [
    url(r'^method/yandex/complete/', yandex_donate_complete, name='yandex_donate_complete'),
    url(r'^method/yandex/', yandex_receive_payment, name='yandex_receive_payment'),
]
