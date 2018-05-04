from django.utils import timezone
from django.contrib import messages
from django.shortcuts import render, redirect
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required

from unitedcp.funcs import get_client_ip
from unitedcp.guides.models import (UserGuide, UserGuideReward, UserGuideTag)
from unitedcp.guides.forms import (GuideSearchForm, GuideAddForm, GuideAddTagForm)


@csrf_protect
def guides_main_page(request):
    context = {
        'GuidesRewards': UserGuideReward.objects.values().all(),
        'GuidesList': UserGuide.objects.values().filter().all(),
        'SearchForm': GuideSearchForm()
    }

    if request.method == "POST":
        form = GuideSearchForm(request.POST)
        if form.is_valid():
            word = form.cleaned_data.get('guide_search')
            search_list = UserGuide.objects.values().filter(title__contains=word).all()
            context['GuidesList'] = search_list if search_list.exists() else False
        else:
            messages.add_message(request, messages.WARNING, form.errors)
    return render(request, 'default/guides/main.html', context)


@csrf_protect
@login_required
def guides_add_page(request):
    if request.method == "POST":
        form = GuideAddForm(request.POST, request.FILES)
        tag_form = GuideAddTagForm(request.POST)
        if form.is_valid() and tag_form.is_valid():
            title = form.cleaned_data.get('title')
            category = form.cleaned_data.get('category')
            description = form.cleaned_data.get('description')
            tags = tag_form.cleaned_data.get('tag')
            user = request.user

            try:
                main_image = request.FILES['main_image']
            except KeyError:
                main_image = ''

            UserGuide.objects.create(
                title=title,
                category=category,
                description=description,
                main_image=main_image,
                user=user,
                date=timezone.now()
            )
            last_guide = UserGuide.objects.last()

            for tag in tags.split(','):
                UserGuideTag.objects.create(
                    guide_id=last_guide,
                    tag=tag
                )

            messages.add_message(request, messages.WARNING, _('Guide \'{}\' successfully added, wait for moderation.'.format(title)))
            return redirect(guides_main_page)
        else:
            messages.add_message(request, messages.WARNING, form.errors)
            messages.add_message(request, messages.WARNING, tag_form.errors)
            return redirect(guides_add_page)
    return render(request, 'default/guides/add_guide.html', {
        'GuideCreateForm': GuideAddForm(),
        'GuideTagForm': GuideAddTagForm(),
        'GuidesRewards': UserGuideReward.objects.values().all(),
    })


@login_required
def apply_guide(request, guide_id):
    if not request.user.is_staff:
        return redirect(guides_main_page)

    try:
        guide = UserGuide.objects.get(pk=guide_id)
    except UserGuide.DoesNotExist or UserGuide.MultipleObjectsReturned:
        return redirect(guides_main_page)

    try:
        reward = UserGuideReward.objects.get(category=guide.category)
    except UserGuideReward.DoesNotExist or UserGuideReward.MultipleObjectsReturned:
        return redirect(guides_main_page)

    guide.apply_guide(request.user.id, reward.reward_id, reward.reward_amount, get_client_ip(request))
    messages.add_message(request, messages.WARNING, _('Guide \'{}\' successfully applied.'.format(guide.title)))
    return redirect(guides_main_page)


@csrf_protect
@login_required
def guide_view_page(request, guide_id):
    try:
        guide = UserGuide.objects.get(pk=guide_id)
    except UserGuide.DoesNotExist or UserGuide.MultipleObjectsReturned:
        messages.add_message(request, messages.WARNING, _('Guide not found.'))
        return redirect(guides_main_page)

    if guide.on_moderation:
        messages.add_message(request, messages.WARNING, _('Guide on moderation.'))
        return redirect(guides_main_page)

    return render(request, 'default/guides/view_guide.html', {'GuideInfo': guide})
