from django.conf.urls import url, include
from unitedcp.staff.views import *


urlpatterns = [
    # Main Page:
    url(r'^main/', staff_panel, name='staff_index'),

    # News
    url(r'^news/', include('unitedcp.staff.news.urls')),

    # Logs
    url(r'^logs/main/', log_main_page, name='staff_logs_main'),
]
