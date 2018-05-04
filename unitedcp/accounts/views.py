from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required

from unitedcp.funcs import *
from unitedcp.views import main_page
from unitedcp.models import *
from unitedcp.ragnarok.funcs import *
from unitedcp.ragnarok.forms import (GameRegisterForm, SetMasterAccountForm)
from unitedcp.accounts.models import PromoCodes
from .funcs import *
from .forms import *
from ragnarokcp.settings.base import *


@login_required
def control_panel(request):
    context = {
        'GameAccounts': get_game_accounts(request.user.id),
        'Donations': {
            'YandexMoney': {
                'wallet': YANDEX_MONEY_WALLET,
                'rate': DONATION_RATE,
                'enabled': YANDEX_MONEY_ENABLED
            },
        },
        'UserChangePasswordForm': UserChangePasswordForm(),
        'DefaultMap': DEFAULT_MAP,
        'RecentActions': get_latest_actions(request.user.id, 5),
        'ChangeEmailForm': UserChangeEmailForm(),
        'Characters': get_account_characters(request.user.id),
        'ProfileInfo': UserProfile.objects.get_or_create(user=request.user)
    }
    return render(request, 'default/panel/index.html', context)


@csrf_protect
@login_required
def user_profile(request):
    if request.method == "POST":
        form = UserProfileForm(request.POST, request.FILES)
        personal_form = MainUserForm(request.POST)
        user = User.objects.get(username=request.user.username)
        if form.is_valid():
            phone = form.cleaned_data.get('phone')
            try:
                avatar = request.FILES['user_avatar']
            except KeyError:
                avatar = ''

            viewable = form.cleaned_data.get('viewable')
            notifications = form.cleaned_data.get('receive_notifications')
            first_name = personal_form['first_name'].value()
            last_name = personal_form['last_name'].value()
            email = personal_form['email'].value()
            password = personal_form['password'].value()

            UserProfile.objects.filter(user=request.user).update(
                phone=phone,
                user_avatar=avatar,
                viewable=viewable,
                receive_notifications=notifications
            )

            user.first_name = first_name
            user.last_name = last_name
            user.email = email

            if password:
                user.set_password(password)
            user.save()

            messages.add_message(request, messages.SUCCESS, _('Profile successfully updated'))
            return redirect(control_panel)
        else:
            messages.add_message(request, messages.SUCCESS, form.errors)
            return redirect(control_panel)
    profile_data = UserProfile.objects.values('viewable', 'user_avatar', 'phone', 'receive_notifications').filter(user=request.user).first()
    main_user_data = User.objects.values('email', 'first_name', 'last_name').filter(username=request.user.username).first()
    return render(request, 'default/panel/profile.html', {
        'ProfileForm': UserProfileForm(profile_data),
        'MainProfileForm': MainUserForm(main_user_data)
    })


@csrf_protect
@login_required
def user_change_password(request):
    if request.method == "POST":
        form = UserChangePasswordForm(request.POST)

        if form.is_valid():
            old_pass = form.cleaned_data.get('old_password')
            new_pass = form.cleaned_data.get('new_password')

            try:
                user = User.objects.get(username=request.user.username)
            except User.DoesNotExist:
                messages.add_message(request, messages.WARNING, _('Something went wrong, please contact with administration'))
                return redirect(control_panel)

            if old_pass == new_pass:
                messages.add_message(request, messages.WARNING, _('Old password same as new'))
                return redirect(control_panel)

            if user.check_password(old_pass):
                user.set_password(new_pass)
                user.save()
                messages.add_message(request, messages.SUCCESS, _('Password successfully changed'))
                PanelLogs.objects.create(action='Master account password changed', ip=get_client_ip(request), user=request.user.id, code=2)
                logout(request)
                return redirect(main_page)
            else:
                PanelLogs.objects.create(action='User password change incorrect old password', ip=get_client_ip(request), user=request.user.id, code=2)
                messages.add_message(request, messages.WARNING, _('Incorrect password'))
                return redirect(control_panel)
        else:
            messages.add_message(request, messages.WARNING, _('Incorrect data, please try again.'))
            return redirect(control_panel)
    else:
        return redirect(control_panel)


@csrf_protect
@login_required
def user_change_email(request):
    if request.method == "POST":
        form = UserChangeEmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('new_email')
            key = get_verification_key()

            UserVerification.objects.create(
                key=key,
                user=request.user.id,
                verification_date=timezone.now(),
                key_expires=timezone.now() + timezone.timedelta(days=7),
                action=2,
                new_value=email
            )

            send_mail(
                subject='{} verification'.format(SERVER_NAME),
                message='Welcome to {}'.format(SERVER_NAME),
                from_email='noreply@alfheim.ro',
                recipient_list=[email],
                html_message=VERIFY_TEMPLATE.format(SERVER_NAME, SERVER_URL + '/verify/{}/2/'.format(key), SERVER_URL,
                                                             SERVER_URL, 'want to change your master account E-Mail')
            )
        else:
            messages.add_message(request, messages.INFO, form.errors)
    return redirect(control_panel)
@csrf_protect
@login_required
def promo_page(request):

    if request.method == "POST":
        form = PromoPageForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data.get('code')

            try:
                promo = PromoCodes.objects.get(code=code)
            except PromoCodes.DoesNotExist:
                messages.add_message(request, messages.INFO, 'Такого кода не существует.')
                return redirect(promo_page)

            UserRewards.objects.create(
                user=request.user,
                reward_id=promo.reward,
                reward_amount=promo.amount
            )

            promo.delete()
            messages.add_message(request, messages.INFO, 'Код успешно активирован, поговорите с NPC Халявщик в Пронтере.')
            return redirect(promo_page)
        else:
            messages.add_message(request, messages.INFO, form.errors)
            return redirect(promo_page)

    return render(request, 'default/panel/promos.html', {
        'PromoForm': PromoPageForm(),
        'MyRewards': UserRewards.objects.filter(user=request.user).all()
    })

