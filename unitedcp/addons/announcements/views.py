from django.utils import timezone
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required

from unitedcp.accounts.models import UserProfile
from unitedcp.addons.announcements.forms import *
from unitedcp.accounts.views import control_panel


def get_comments(announce_id):
    comments = UserAnnouncementsComments.objects.values().filter(announce=announce_id)
    return comments


def annoucement_list(request):
    return render(request, 'announcements/announce_list.html')


@csrf_protect
@login_required(login_url='/system/auth/login/')
def annoucement_add(request):
    try:
        profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        messages.add_message(request, messages.WARNING, 'Please, select main character in Account Overview!')
        return redirect(control_panel)

    if not profile.main_character:
        messages.add_message(request, messages.WARNING, 'Please, select main character in Account Overview!')
        return redirect(control_panel)

    if request.method == "POST":
        form = UserAnnouncementsForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            message = form.cleaned_data.get('message')
            announce_type = form.cleaned_data.get('announce_type')

            UserAnnouncements.objects.create(
                user=request.user.id,
                title=title,
                announce_type=announce_type,
                announce_date=timezone.now(),
                main_character=profile.main_character,
                message=message,
                updated_date=timezone.now()
            )
            messages.add_message(request, messages.WARNING, 'Announcement successfully added.')
            return redirect(annoucement_list)
        else:
            messages.add_message(request, messages.INFO, form.errors)
            return redirect(annoucement_list)
    else:
        return render(request, 'announcements/announce_add.html', {'AddForm': UserAnnouncementsForm(), 'MainChar': profile.main_character})


def announcement_view(request, aid):
    if request.method == "POST":
        form = UserAnnouncementsCommentForm(request.POST)
        if form.is_valid():
            comment = form.cleaned_data.get('message')

            try:
                profile = UserProfile.objects.get(user=request.user)
            except UserProfile.DoesNotExist:
                messages.add_message(request, messages.WARNING, 'Please, select main character in Account Overview!')
                return redirect(control_panel)

            if not profile.get_main_character():
                messages.add_message(request, messages.WARNING, 'Please, select main character in Account Overview!')
                return redirect(control_panel)

            try:
                instance = UserAnnouncements.objects.get(id=aid)
            except UserAnnouncements.DoesNotExist:
                messages.add_message(request, messages.WARNING, 'Announcement not found!')
                return redirect(annoucement_list)

            UserAnnouncementsComments.objects.create(
                user=request.user.id,
                announce=instance,
                character=profile.get_main_character(),
                message=comment,
                comment_date=timezone.now()
            )

            messages.add_message(request, messages.WARNING, 'Comment successfully added')
            return redirect(annoucement_list)
    else:
        announce = UserAnnouncements.objects.values_list('id', 'message', 'title', 'main_character', 'announce_type', 'announce_date', 'user', 'updated_date').filter(
            id=aid).first()
        if not announce:
            messages.add_message(request, messages.WARNING, 'Announcement not found!')
            return redirect(annoucement_list)

        return render(request, 'announcements/announce_view.html', {
            'Announce': announce,
            'CommentForm': UserAnnouncementsCommentForm(),
            'Comments': get_comments(aid)
        })


def announcement_update(request, aid):
    try:
        announce = UserAnnouncements.objects.get(id=aid)
    except UserAnnouncements.DoesNotExist:
        messages.add_message(request, messages.WARNING, 'Announcement not found!')
        return redirect(annoucement_list)

    announce.updated_date = timezone.now()
    announce.save()
    messages.add_message(request, messages.WARNING, 'Announcement updated.')
    return redirect(annoucement_list)
