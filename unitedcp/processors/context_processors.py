from ragnarokcp.settings.base import *
from django.db import connection
from unitedcp.funcs import server_status, get_discord_online
from unitedcp.forms import (LoginForm, UserPasswordResetForm)


def server_name(request):
    return {
        'ServerName': SERVER_NAME,
        'Queries': len(connection.queries),
        'SocialLinks': SOCIAL_LINKS,
        'LoginForm': LoginForm(),
        'ResetForm': UserPasswordResetForm(),
        'ServerStatus': server_status(),
        'DiscordOnline': get_discord_online(),
        'peak': 0
    }
