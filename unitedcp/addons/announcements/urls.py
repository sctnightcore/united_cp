from django.conf.urls import url
from .views import *
from .api import *

urlpatterns = [
    url(r'^index/', annoucement_list, name='announce_list'),
    url(r'^add/', annoucement_add, name='announce_add'),
    url(r'^view/(?P<aid>.*)/', announcement_view, name='announce_view'),
    url(r'^update/(?P<aid>.*)/', announcement_update, name='announce_update'),
    url(r'^list/', Announcements.as_view()),
]
