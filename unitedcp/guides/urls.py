from django.conf.urls import url, include
from unitedcp.guides.views import *

urlpatterns = [
    url(r'^main/', guides_main_page, name='guides_main'),
    url(r'^add/', guides_add_page, name='guides_add'),
    url(r'^apply/(?P<guide_id>.*)/', apply_guide, name='apply_guide'),
    url(r'^view/(?P<guide_id>.*)/', guide_view_page, name='view_guide'),
]
