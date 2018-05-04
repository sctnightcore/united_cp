from ragnarokcp import settings
from django.db import connection
from unitedcp.funcs import server_status, get_discord_online
from unitedcp.forms import (LoginForm, UserPasswordResetForm)
from unitedcp.models import CPHighPeak


def server_name(request):
    return {
        'ServerName': settings.SERVER_NAME,
        'Queries': len(connection.queries),
        'SocialLinks': settings.SOCIAL_LINKS,
        'LoginForm': LoginForm(),
        'ResetForm': UserPasswordResetForm(),
        'ServerStatus': server_status(),
        'DiscordOnline': get_discord_online(),
        'peak': 0
    }
