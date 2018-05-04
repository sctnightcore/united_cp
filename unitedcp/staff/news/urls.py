from django.conf.urls import url, include
from unitedcp.staff.news.views import *


urlpatterns = [
    # Main Page:
    url(r'^main/', news_page, name='staff_news_main'),
    url(r'^add/', news_page_add, name='staff_news_add'),
]
