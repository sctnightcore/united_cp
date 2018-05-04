from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required

from unitedcp.donations.models import *
from unitedcp.accounts.views import control_panel


@login_required
def staff_panel(request):
    if not request.user.is_staff:
        return redirect(control_panel)

    return render(request, 'united/staff/donation_main_modal.html')


@login_required
def log_main_page(request):
    if not request.user.is_staff:
        return redirect(control_panel)

    context = {
        'DonationLogs': DonationsLog.objects.values().order_by('-date').all()
    }
    return render(request, 'united/staff/logs/donation_main_modal.html', context)
