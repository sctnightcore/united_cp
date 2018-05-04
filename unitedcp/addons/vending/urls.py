from django.conf.urls import url
from .views import *
from .api import *

urlpatterns = [
    url(r'^index/', vending_index, name='vending_index'),
    url(r'^list/', VendingsList.as_view()),
    url(r'^view/(\d+)/', view_vendor_byid, name='vending_view'),
]
