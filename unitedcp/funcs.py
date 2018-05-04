import random
import string
import socket
import requests
import datetime
from django.utils import timezone
from user_agents import parse

from django.core.cache import cache
from django.utils.translation import ugettext_lazy as _

from ragnarokcp.settings.base import (EVENTER, SERVER_ONLINE_UPDATE)
from unitedcp.ragnarok.models import Char, Guild, MvpRating
from django.db.models import Sum


def get_verification_key():
    key = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(20)])
    return key


def server_status():
    # sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #
    # if not cache.get('ServerStatus'):
    #     map_server = sock.connect_ex((SERVER_IP, MAP_PORT))
    #     char_server = sock.connect_ex((SERVER_IP, CHAR_PORT))
    #     login_server = sock.connect_ex((SERVER_IP, LOGIN_PORT))
    #     sock.close()
    #     status = (map_server, char_server, login_server)
    #     cache.set('ServerStatus', status, SERVER_STATUS_UPDATE)
    # else:
    #     status = cache.get('ServerStatus')
    #
    # if not cache.get('ServerOnline'):
    #     population = Char.objects.filter(online=1).all().count()
    #     cache.set('ServerOnline', population, SERVER_ONLINE_UPDATE)
    # else:
    #     population = cache.get('ServerOnline')
    #
    # map_server = True if status[0] == 0 else False
    # char_server = True if status[1] == 0 else False
    # login_server = True if status[2] == 0 else False

    return {
        'MapServer': 0,
        'CharServer': 0,
        'LoginServer': 0,
        'Online': 0
    }


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def get_client_browser(request):
    ua_string = request.META.get('HTTP_USER_AGENT')
    user_agent = parse(ua_string)

    return user_agent.browser.family


def get_client_device(request):
    ua_string = request.META.get('HTTP_USER_AGENT')
    user_device = parse(ua_string)

    return user_device.device.family


def get_client_os(request):
    ua_string = request.META.get('HTTP_USER_AGENT')
    user_os = parse(ua_string)

    return user_os.os.family


def get_discord_online():
    if not cache.get('DiscordOnline'):
        value = requests.get('https://discordapp.com/api/guilds/348869172698284032/embed.json')
        r = value.json()
        updated = timezone.now()
        cache.set('DiscordOnline', r, SERVER_ONLINE_UPDATE)
        cache.set('DiscordUpdated', updated, SERVER_ONLINE_UPDATE)
    else:
        r = cache.get('DiscordOnline')
        updated = cache.get('DiscordUpdated')
    return {
        'Online': len(r['members']),
        'Updated': updated
    }


def get_index_top():
    characters = Char.objects.values('name', 'base_level', 'job_level', 'base_exp', 'job_exp', 'guild_id',
                                     'class_field', 'account_id__sex').filter(
        account_id__group_id__lt=EVENTER).order_by(
        '-base_level',
        '-base_exp',
        '-job_level',
        '-job_exp',
        'char_id')[:5]

    if not characters.exists():
        characters = None

    zeny_characters = Char.objects.values('name', 'base_level', 'job_level', 'class_field', 'zeny', 'guild_id',
                                          'account_id__sex').filter(
        account_id__group_id__lt=EVENTER).order_by('-zeny', '-base_level', '-base_exp', '-job_level',
                                                            '-job_exp', 'char_id')[:5]
    if not characters:
        zeny_characters = None

    mvp_characters = MvpRating.objects.values('char_id__name', 'score', 'mvp_amount', 'char_id__guild_id',
                                              'char_id__class_field').filter(
        char_id__account_id__group_id__lt=EVENTER).order_by('-score', '-mvp_amount', 'char_id')[:5]
    if not characters:
        mvp_characters = None

    guilds = Guild.objects.values('guild_id', 'guild_name', 'guild_lv', 'average_lv', 'max_member', 'exp',
                                  'master').filter(
        char_id__account_id__group_id__lt=EVENTER).order_by('-guild_lv', '-exp', '-average_lv', '-max_member',
                                                                     'next_exp')[:3]

    if not guilds:
        guilds = None
    return {
        'Top5Players': characters,
        'Top3Guilds': guilds,
        'Top5Zeny': zeny_characters,
        'Top5Mvp': mvp_characters
    }


def get_totals():
    mvp = MvpRating.objects.all().aggregate(Sum('mvp_amount'))

    guilds = Guild.objects.all().count()

    opening = datetime.date(2017, 9, 10)
    today = datetime.date.today()

    return {
        'MvpKilled': mvp,
        'GuildCount': guilds,
        'DaysFromOpening': (today - opening).days
    }
