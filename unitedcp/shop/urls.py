from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^main/', shop_main, name='shop_main'),
    url(r'^item/view-(?P<item>.*)/', shop_view_item, name='shop_view_item')
]
