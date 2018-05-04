from random import choice
from django.db.models import Q
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from django.utils.translation import ugettext_lazy as _
from django.http import Http404, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

from unitedcp.forms import *
from unitedcp.funcs import *
from unitedcp.models import *
from unitedcp.staff.news.models import *
from unitedcp.ragnarok.funcs import *


# Main Page
def home_page(request):
    return render(request, 'default/startpage/index.html')


def main_page(request):
    context = {
        'LoginForm': LoginForm(),
        'RegisterFrom': RegisterForm(),
        'FastRegisterForm': FastRegisterForm(),
        'LatestNews': CPNews.objects.values().all()[:3][::-1],
        'PlayersCount': User.objects.filter(is_active=True).count(),
        'Random': timezone.now(),
        'bgNumber': choice([7, 8]),
        'indexTop': '',
        'totals': '',
        'GameAccounts': get_game_accounts(request.user.id),
        'Characters': get_account_characters(request.user.id),
    }
    return render(request, 'default/index.html', context)


@csrf_protect
def auth_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                PanelLogs.objects.create(action='Successfull logged in, user: {}'.format(username),
                                         ip=get_client_ip(request), code=1, user=user.id,
                                         agent=get_client_browser(request), device=get_client_device(request),
                                         os=get_client_os(request))
                return redirect(main_page)
            else:
                PanelLogs.objects.create(action='Invalid credentials for user: {}'.format(username),
                                         ip=get_client_ip(request), code=1)
                messages.add_message(request, messages.ERROR,
                                     _('Invalid credentials. Be sure that your account activated'))
                return redirect(auth_login)
        else:
            messages.add_message(request, messages.INFO, form.errors)
    return redirect(main_page)


@login_required
def auth_logout(request):
    logout(request)
    return redirect(main_page)


@csrf_protect
def auth_register(request):
    if request.method == "POST":
        form = FastRegisterForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data.get('email')
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            verify_key = get_verification_key()
            user = User.objects.filter(Q(username=username) | Q(email=email)).all()
            try:
                gender = form.cleaned_data.get('gender')
            except Exception as Exp:
                gender = None

            if user.exists():
                messages.add_message(request, messages.INFO, _('User already exists'))
                return redirect(main_page)

            User.objects.create_user(username, email, password, is_active=True)
            last_user = User.objects.values('id').last()
            UserVerification.objects.create(
                user=User.objects.get(pk=last_user['id']),
                key=verify_key,
                verification_date=timezone.now(),
                key_expires=timezone.now() + timezone.timedelta(days=7),
                action=1
            )

            if gender is not None:
                Login.objects.create_game_account(
                    userid=username,
                    user_pass=password,
                    sex=gender,
                    email=email,
                    master_account=User.objects.get(pk=last_user['id'])
                )

            messages.add_message(request, messages.INFO, _('User successfully registered!'))
            return redirect(main_page)
        else:
            messages.add_message(request, messages.INFO, form.errors)
            return redirect(main_page)
    else:
        return render(request, 'default/sign-up.html', {
            'FastRegisterForm': FastRegisterForm(),
            'MinPassword': 4,
            'MaxPassword': settings.MAX_PASSWORD_LENGTH,
            'MinUsername': settings.MIN_USERNAME_LENGTH,
            'MaxUsername': settings.MAX_USERNAME_LENGTH,
        })


@csrf_protect
def user_password_reset(request):
    if request.method == "POST":
        form = UserPasswordResetForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data.get('email')

            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                messages.add_message(request, messages.WARNING, 'User not found')
                return redirect(auth_login)

            new_password = get_verification_key()
            send_mail(
                subject='{} password reset'.format(settings.SERVER_NAME),
                message='Welcome to {}'.format(settings.SERVER_NAME),
                from_email='noreply@alfheim.ro',
                recipient_list=[email],
                html_message='<p>Login: {}</p> <p>New password: {}</p>, <p>Please, change password as soon as possible!</p>'.format(
                    user.username, new_password)
            )

            user.set_password(new_password)
            user.save()
            messages.add_message(request, messages.INFO, 'New password was sent to your E-Mail.')
            return redirect(auth_login)
        else:
            messages.add_message(request, messages.INFO, form.errors)
            return redirect(auth_login)
    else:
        return redirect(auth_login)


def handler404(request):
    return HttpResponseBadRequest("Not found. 404.")


def read_news(request, article_id):
    try:
        news = CPNews.objects.get(pk=article_id)
    except CPNews.DoesNotExist:
        raise Http404("Article does not exist")

    images = CPNewsImages.objects.values().filter(news_id=article_id).all()
    if not images.exists():
        images = False

    return render(
        request,
        'default/read_news.html',
        {
            'ViewNews': news,
            'ViewImagesSlider': images
        })


def user_verification(request, key, action):
    if not key or not action:
        raise Http404

    try:
        verification = UserVerification.objects.get(key=key, action=action)
    except UserVerification.DoesNotExist or UserVerification.MultipleObjectsReturned:
        messages.add_message(request, messages.WARNING, _('Incorrect link'))
        return redirect(main_page)

    if timezone.now() > verification.key_expires:
        messages.add_message(request, messages.WARNING, _('Key time expires.'))
        return redirect(main_page)

    if action == '1':
        if verification.user.is_active:
            messages.add_message(request, messages.WARNING, _('This account already active.'))
            return redirect(main_page)

        verification.user.is_active = True
        verification.user.save()
        verification.delete()
        messages.add_message(request, messages.WARNING, _('User successfully activated.'))

        if settings.USE_XENFORO_API:
            r = requests.get(
                'http://127.0.0.1/api.php?action=register&hash={0}&username={1}&password={2}&email={3}&group=Player'.format(
                    settings.XENFORO_API,
                    verification.user.username,
                    verification.user.password,
                    verification.user.email
                )
            )
            print(r.status_code)
            print(r.text)

    elif action == '2':
        new_email = verification.new_value
        old_email = verification.user.email

        accounts = Login.objects.values('account_id').filter(master_account=verification.user.id).all()
        for account in accounts:
            try:
                game_account = Login.objects.get(account_id=account)
            except Login.DoesNotExist:
                game_account = None

            if game_account:
                game_account.email = new_email
                game_account.save()

        verification.delete()
        PanelLogs.objects.create(action='User email changed from {} to {}'.format(old_email, new_email),
                                 ip=get_client_ip(request), user=verification.user.id, code=4)
        messages.add_message(request, messages.WARNING, _('E-Mail successfully changed.'))
    else:
        messages.add_message(request, messages.WARNING, _('Unknown action.'))
    return redirect(main_page)
