from django.conf.urls import url
from unitedcp.ragnarok.views import *

urlpatterns = [
    url(r'^register/', register_game_account, name='auth_game_register'),
    url(r'^manage/(?P<account_id>.*)/', game_account_settings, name='game_account_settings'),
    url(r'^character/(?P<char_id>.*)/set/', set_main_character, name='set_main_character'),
    url(r'^character/(?P<char_id>.*)/reset/position/', char_reset_position, name='reset_position'),
    url(r'^character/(?P<char_id>.*)/reset/look/', char_reset_look, name='reset_look'),
    url(r'^add-exist/', add_game_account, name='set_master_account'),
    url(r'^character/(?P<char_id>.*)/(?P<account_id>.*)/delete/', delete_character, name='delete_character'),
    url(r'^character/del/', del_main_character, name='del_main_character'),
    url(r'^character/(?P<char_id>.*)/profile/', view_character, name='character_profile'),
]
