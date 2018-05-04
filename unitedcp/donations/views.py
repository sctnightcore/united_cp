from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import (csrf_exempt, csrf_protect)
from django.contrib.auth.decorators import login_required

from .yandex import *
from unitedcp.views import main_page


@csrf_exempt
def yandex_receive_payment(request):
    if request.method != 'POST':
        return redirect(main_page)

    yandex_donate(request)
    return HttpResponse(status=200)


@login_required
def yandex_donate_complete(request):
    return render(request, 'default/panel/donations/../templates/default/panel/new/modals/donation_complete.html')
