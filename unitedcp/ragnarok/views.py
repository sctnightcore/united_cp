from django.db.models import Q
from django.contrib import messages
from django.shortcuts import render, redirect
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required

from unitedcp.funcs import *
from unitedcp.models import *
from unitedcp.views import main_page
from unitedcp.accounts.views import control_panel
from unitedcp.accounts.models import UserProfile

from .models import *
from .forms import *


@login_required
def char_reset_position(request, char_id):
    try:
        char = Char.objects.get(char_id=char_id)
    except Char.DoesNotExist:
        messages.add_message(request, messages.WARNING, _('Character not found'))
        return redirect(control_panel)

    if char.account_id.master_account_id != request.user.id:
        messages.add_message(request, messages.WARNING, _('You can\'t manage this account'))
        return redirect(control_panel)

    char.last_map = settings.DEFAULT_MAP
    char.last_x = settings.DEFAULT_X
    char.last_y = settings.DEFAULT_Y
    char.save()
    messages.add_message(request, messages.WARNING,
                         _('Character {} moved to {}'.format(char.name, settings.DEFAULT_MAP)))
    PanelLogs.objects.create(action='Character {} position resetted'.format(char.name), ip=get_client_ip(request),
                             user=request.user.id, code=4)
    return redirect(control_panel)


@login_required
def char_reset_look(request, char_id):
    try:
        char = Char.objects.get(char_id=char_id)
    except Char.DoesNotExist:
        messages.add_message(request, messages.WARNING, _('Character not found.'))
        return redirect(control_panel)

    if char.account_id.master_account_id is not request.user.id:
        messages.add_message(request, messages.WARNING, _('You can\'t manage this account'))
        return redirect(control_panel)

    char.hair = 0
    char.hair_color = 0
    char.clothes_color = 0
    char.head_top = 0
    char.head_mid = 0
    char.head_bottom = 0
    char.robe = 0
    char.save()
    messages.add_message(request, messages.WARNING,
                         'All clothes colors, hair style and hair colors resetted for {}'.format(char.name))
    PanelLogs.objects.create(action='Character {} look resetted'.format(char.name), ip=get_client_ip(request),
                             user=request.user.id, code=4)
    return redirect(control_panel)


@csrf_protect
@login_required
def game_account_settings(request, account_id):
    try:
        account_info = Login.objects.get(account_id=account_id)
    except Login.DoesNotExist:
        messages.add_message(request, messages.WARNING, _('Account not found.'))
        return redirect(control_panel)

    if request.user.id != account_info.master_account_id:
        messages.add_message(request, messages.WARNING, _('You can\'t manage this account.'))
        return redirect(control_panel)

    if request.method == "POST":
        form = GameChangePasswordForm(request.POST)
        if form.is_valid():
            new_passwd = form.cleaned_data.get('new_password')
            account_info.change_password(new_passwd)
            messages.add_message(request, messages.WARNING, _('Password has successfully been changed'))
            return redirect(control_panel)
    else:
        return render(request, 'default/panel/account_manager.html',
                      {'GameAccount': account_info, 'ChangePassForm': GameChangePasswordForm()})


@csrf_protect
@login_required
def set_main_character(request, char_id):
    UserProfile.objects.get(user=request.user).set_main_character(char_id)
    messages.add_message(request, messages.WARNING, _('Main character updated'))
    return redirect(control_panel)


@csrf_protect
@login_required
def del_main_character(request):
    UserProfile.objects.get(user=request.user).del_main_character()
    messages.add_message(request, messages.WARNING, _('Main character updated'))
    return redirect(control_panel)


@csrf_protect
@login_required
def register_game_account(request):
    if request.method == "POST":
        form = GameRegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            gender = form.cleaned_data.get('gender')

            try:
                user_check = Login.objects.get(userid=username)
            except Login.DoesNotExist:
                user_check = False

            if user_check:
                messages.add_message(request, messages.WARNING, _('This login already exist.'))
                return redirect(register_game_account)

            Login.objects.create_game_account(userid=username, user_pass=password, email=request.user.email, sex=gender,
                                              master_account=request.user)
            PanelLogs.objects.create(action='Game account created', ip=get_client_ip(request), user=request.user.id,
                                     code=3)
            messages.add_message(request, messages.INFO, _('Game account successfully created.'))
            return redirect(register_game_account)
        else:
            messages.add_message(request, messages.INFO, form.errors)
            return redirect(register_game_account)
    else:
        return render(request, 'default/panel/create_game_account.html', {
            'SetMasterAccountForm': SetMasterAccountForm(),
            'GameRegisterForm': GameRegisterForm(),
        })


@csrf_protect
@login_required
def add_game_account(request):
    if request.method == "POST":
        form = SetMasterAccountForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            try:
                game_account = Login.objects.get(userid=username)
            except Login.DoesNotExist:
                messages.add_message(request, messages.INFO, _('Game account doesn\'t found.'))
                return redirect(register_game_account)

            if game_account.check_passwd(password):
                if game_account.set_master_account(request.user.id):
                    messages.add_message(request, messages.INFO, _('Game account added.'))
                else:
                    messages.add_message(request, messages.INFO, _('This account already have master id.'))
            else:
                messages.add_message(request, messages.INFO, _('Incorrect password.'))
        else:
            messages.add_message(request, messages.INFO, form.errors)
    return redirect(register_game_account)


@csrf_protect
@login_required
def delete_character(request, char_id, account_id):
    try:
        character = Char.objects.get(char_id=char_id)
    except Char.DoesNotExist:
        messages.add_message(request, messages.WARNING, _('Character not found.'))
        return redirect(control_panel)
    try:
        account_info = Login.objects.get(account_id=account_id)
    except Login.DoesNotExist:
        messages.add_message(request, messages.WARNING, _('Account not found.'))
        return redirect(control_panel)

    if request.user.id != account_info.master_account_id:
        messages.add_message(request, messages.WARNING, _('You can\'t manage this account.'))
        return redirect(control_panel)

    if character.mother or character.father:
        Char.objects.filter(Q(char_id=character.mother) | Q(char_id=character.father)).update(child=0)
        Skill.objects.filter(Q(char_id=character.mother) | Q(char_id=character.father), id=410).delete()

    Pet.objects.filter(char_id=character.char_id, incubate=0).delete()
    if character.homun_id:
        Homunculus.objects.filter(char_id=character.char_id).delete()

    Quest.objects.filter(char_id=character.char_id).delete()
    Friends.objects.filter(char_id=character.char_id).delete()
    Friends.objects.filter(friend_id=character.char_id).delete()
    Hotkey.objects.filter(char_id=character.char_id).delete()
    Inventory.objects.filter(char_id=character.char_id).delete()
    CartInventory.objects.filter(char_id=character.char_id).delete()
    Memo.objects.filter(char_id=character.char_id).delete()
    CharRegNumDb.objects.filter(char_id=character.char_id).delete()
    CharRegStrDb.objects.filter(char_id=character.char_id).delete()
    Skill.objects.filter(char_id=character.char_id).delete()
    ScData.objects.filter(char_id=character.char_id).delete()
    Char.objects.filter(char_id=character.char_id).delete()
    GuildMember.objects.filter(char_id=character.char_id).delete()

    try:
        guild = Guild.objects.get(master=character.name)
    except Guild.DoesNotExist:
        guild = None

    if guild:
        Guild.objects.filter(master=character.name).delete()
        GuildMember.objects.filter(guild_id=guild.guild_id).delete()
        GuildAlliance.objects.filter(guild_id=guild.guild_id).delete()
        GuildAlliance.objects.filter(alliance_id=guild.guild_id).delete()
        GuildCastle.objects.filter(guild_id=guild.guild_id).delete()
        GuildPosition.objects.filter(guild_id=guild.guild_id).delete()
        GuildSkill.objects.filter(guild_id=guild.guild_id).delete()

    UserProfile.objects.filter(ro_character=character.char_id).update(ro_character=0)
    messages.add_message(request, messages.WARNING, 'Персонаж успешно удален')
    return redirect(control_panel)


def view_character(request, char_id):
    char_is_mine = False

    try:
        character_data = Char.objects.get(char_id=char_id)
    except Char.DoesNotExist:
        messages.add_message(request, messages.WARNING, 'Персонаж не найден')
        return redirect(main_page)

    master_id = character_data.account_id.master_account_id
    if request.user.id and request.user.id == master_id:
        char_is_mine = True

    if UserProfile.objects.get(user=master_id).can_view() and not char_is_mine:
        messages.add_message(request, messages.WARNING, 'Игрок не разрешил просматривать его профиль')
        return redirect(main_page)

    friends_data = Friends.objects.values().filter(friend_id=char_id).all()
    guild_data = Guild.objects.values().filter(guild_id=character_data.guild_id).all()
    pet_data = Pet.objects.values().filter(char_id=char_id).all()
    hom_data = Homunculus.objects.values().filter(char_id=char_id).all()
    memo_data = Memo.objects.values().filter(char_id=char_id).all()
    cd_data = CharRegNumDb.objects.values().filter(char_id=char_id, key='etower_timer').all()
    quest_data = Quest.objects.values().filter(char_id=char_id).all()
    bg_data = CharBg.objects.values().filter(char_id=char_id).all()
    woe_data = CharWstats.objects.values().filter(char_id=char_id).all()
    woe_log_killer = CharWoeLog.objects.values().filter(killer_id=char_id).order_by('-time').all()[:10]
    woe_log_killed = CharWoeLog.objects.values().filter(killed_id=char_id).order_by('-time').all()[:10]
    bg_log_killer = CharBgLog.objects.values().filter(killer_id=char_id).order_by('-time').all()[:10]
    bg_log_killed = CharBgLog.objects.values().filter(killed_id=char_id).order_by('-time').all()[:10]
    skill_data = SkillCount.objects.values().filter(char_id=char_id).order_by('-count').all()[:10]
    bg_skill_data = BgSkillCount.objects.values().filter(char_id=char_id).order_by('-count').all()[:10]

    return render(request, 'default/panel/character_profile.html', {
        'CharacterData': character_data,
        'FriendsData': friends_data,
        'GuildData': guild_data,
        'PetData': pet_data,
        'HomData': hom_data,
        'MemoData': memo_data,
        'CdData': cd_data,
        'QuestData': quest_data,
        'BgData': bg_data,
        'WoeData': woe_data,
        'WoeLogData1': woe_log_killer,
        'WoELogData2': woe_log_killed,
        'BgLogData1': bg_log_killer,
        'BgLogData2': bg_log_killed,
        'SkillData': skill_data,
        'BgSkillData': bg_skill_data,
        'IsMine': char_is_mine
    })
