from django.conf.urls import url

from .views import *

urlpatterns = [
    url(r'^index/', ranking_main, name='ranking_index'),
    url(r'^guilds/', ranking_guild, name='ranking_guild'),
    url(r'^zeny/', ranking_zeny, name='ranking_zeny'),
    url(r'^mvp/', ranking_mvp, name='ranking_mvp'),
    url(r'^woe/', ranking_woe, name='ranking_woe'),
    url(r'^api/woe/', CharWoERanking.as_view()),
    url(r'^api/woe_char_details/', WoECharDetails.as_view()),
    url(r'^api/skill/', SkillRanking.as_view()),
]
