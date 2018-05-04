from .forms import *
from ragnarokcp import settings

from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect

from unitedcp.ragnarok.models import (Char, Guild, CharWstats, MvpRating, CharWoeLog, SkillCount)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.db.models import Count


@csrf_protect
def ranking_main(request):
    if request.method == "POST":
        form = JobSearchForm(request.POST)
        if form.is_valid():
            job = form.cleaned_data.get('class_filter')

            if job == "All":
                characters = Char.objects.values('name', 'base_level', 'job_level', 'base_exp', 'job_exp', 'guild_id',
                                                 'class_field',
                                                 'account_id__sex').filter(
                    account_id__group_id__lt=settings.EVENTER).order_by(
                    '-base_level',
                    '-base_exp',
                    '-job_level',
                    '-job_exp',
                    'char_id')[:25]
            else:
                characters = Char.objects.values('name', 'base_level', 'job_level', 'base_exp', 'job_exp', 'guild_id',
                                                 'class_field',
                                                 'account_id__sex').filter(
                    account_id__group_id__lt=settings.EVENTER, class_field=job).order_by(
                    '-base_level',
                    '-base_exp',
                    '-job_level',
                    '-job_exp',
                    'char_id')[:25]
            if not characters.exists():
                characters = None
            return render(request, 'default/rankings/index.html',
                          {'CharacterRanking': characters, 'FilterForm': JobSearchForm()})
        else:
            return render(request, 'default/rankings/index.html',
                          {'CharacterRanking': False, 'FilterForm': JobSearchForm()})
    else:
        characters = Char.objects.values('name', 'base_level', 'job_level', 'base_exp', 'job_exp', 'guild_id',
                                         'class_field', 'account_id__sex').filter(
            account_id__group_id__lt=settings.EVENTER).order_by(
            '-base_level',
            '-base_exp',
            '-job_level',
            '-job_exp',
            'char_id')[:25]

        if not characters.exists():
            characters = None
        return render(request, 'default/rankings/index.html',
                      {'CharacterRanking': characters, 'FilterForm': JobSearchForm()})


def ranking_guild(request):
    guilds = Guild.objects.values('guild_id', 'guild_name', 'guild_lv', 'average_lv', 'max_member', 'exp',
                                  'master').filter(
        char_id__account_id__group_id__lt=settings.EVENTER).order_by('-guild_lv', '-exp', '-average_lv', '-max_member',
                                                                     'next_exp')[:25]

    if not guilds.exists():
        guilds = None
    return render(request, 'default/rankings/guilds.html', {'GuildRanking': guilds})


def ranking_zeny(request):
    characters = Char.objects.values('name', 'base_level', 'job_level', 'class_field', 'zeny', 'guild_id',
                                     'account_id__sex').filter(
        account_id__group_id__lt=settings.EVENTER).order_by('-zeny', '-base_level', '-base_exp', '-job_level',
                                                            '-job_exp', 'char_id')[:25]
    if not characters.exists():
        characters = None
    return render(request, 'default/rankings/zeny_ranking.html', {'ZenyRanking': characters})


def ranking_mvp(request):
    characters = MvpRating.objects.values('char_id__name', 'score', 'mvp_amount', 'char_id__guild_id',
                                          'char_id__class_field').filter(
        char_id__account_id__group_id__lt=settings.EVENTER).order_by('-score', '-mvp_amount', 'char_id')[:25]
    if not characters.exists():
        characters = None
    return render(request, 'default/rankings/mvp_ranking.html', {'MvpRanking': characters})


def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


class CharWoERanking(APIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        # cur = connection.cursor()
        params = request.query_params
        try:
            woe_date = params['date']
        except KeyError:
            woe_date = '2017-10-01'

        woe_ranking = CharWstats.objects.values('char_id__name', 'char_id', 'char_id__guild_id', 'kill_count',
                                                'death_count', 'score', 'top_damage', 'damage_done',
                                                'damage_received', 'emperium_damage', 'guardian_damage',
                                                'barricade_damage', 'gstone_damage', 'emperium_kill',
                                                'guardian_kill', 'barricade_kill', 'gstone_kill', 'sp_heal_potions',
                                                'hp_heal_potions', 'yellow_gemstones', 'red_gemstones',
                                                'blue_gemstones', 'poison_bottles', 'acid_demostration',
                                                'acid_demostration_fail', 'support_skills_used', 'healing_done',
                                                'wrong_support_skills_used', 'wrong_healing_done', 'sp_used',
                                                'ammo_used', 'char_id__base_level', 'char_id__job_level',
                                                'char_id__class_field', 'spiritb_used'). \
            filter(woe_date=woe_date).order_by('-score', 'char_id').all()
        guild_count = CharWstats.objects.values('char_id__guild_id').annotate(
            memcount=Count('char_id__guild_id')).filter(woe_date=woe_date).order_by('-memcount')
        return Response({'WoERanking': woe_ranking, 'MembersCount': guild_count}, status=200)


class WoECharDetails(APIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        char_id = 0
        params = request.query_params
        try:
            woe_date = params['date']
            char_id = params['char_id']
        except KeyError:
            woe_date = '2017-10-01'

        woe_log_killer = CharWoeLog.objects.values('killed', 'killed_id', 'time', 'skill',
                                                   'killed_id__guild_id').filter(killer_id=char_id, time__range=(
            woe_date + ' 00:00', woe_date + ' 23:59')).order_by('-time').all()
        woe_log_killed = CharWoeLog.objects.values('killer', 'killed_id', 'time', 'skill',
                                                   'killer_id__guild_id').filter(killed_id=char_id, time__range=(
            woe_date + ' 00:00', woe_date + ' 23:59')).order_by('-time').all()
        skill_data = SkillCount.objects.values().filter(char_id=char_id, woe_date__range=(
            woe_date + ' 00:00:00', woe_date + ' 23:59:59')).order_by('-count').all()
        return Response({'WoEKiller': woe_log_killer, 'WoEKilled': woe_log_killed, 'Skills': skill_data}, status=200)


class SkillRanking(APIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        params = request.query_params
        try:
            skill_id = params['skill_id']
            woe_date = params['date']
        except KeyError:
            skill_id = 0
            woe_date = '2017-10-01'

        skill_rank = SkillCount.objects.values('char_id__name', 'skill_id', 'count', 'char_id',
                                               'char_id__guild_id').filter(
            skill_id=skill_id, woe_date__range=(woe_date + ' 00:00:00', woe_date + ' 23:59:59')).order_by(
            '-count').all()
        return Response({'SkillRanking': skill_rank}, status=200)


def ranking_woe(request):
    return render(request, 'default/rankings/woe.html')
