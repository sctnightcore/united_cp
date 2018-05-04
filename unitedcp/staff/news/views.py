from django.contrib import messages
from django.shortcuts import render, redirect
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required

from unitedcp.staff.news.forms import *
from unitedcp.accounts.views import control_panel

@login_required
def news_page(request):
    if not request.user.is_staff:
        return redirect(control_panel)
    return render(request, 'united/staff/news/donation_main_modal.html')


@csrf_protect
@login_required
def news_page_add(request):
    if not request.user.is_staff:
        return redirect(control_panel)

    context = {
        'NewsForm': AddNewsForm,
        'NewsImageForm': AddNewsImagesForm,
        'NewsTagsForm': AddNewsTagsForm,
    }

    if request.method == "POST":
        form = AddNewsForm(request.POST, request.FILES)
        images_form = AddNewsImagesForm(request.FILES)
        tags_form = AddNewsTagsForm(request.POST)

        if form.is_valid() and images_form.is_valid() and tags_form.is_valid():
            title = form.cleaned_data.get('title')
            main_image = request.FILES['main_image']
            type_ = form.cleaned_data.get('news_type')
            description = form.cleaned_data.get('description')
            author = form.cleaned_data.get('author')
            source_url = form.cleaned_data.get('link')
            publish = form.cleaned_data.get('publish')
            tags = tags_form.cleaned_data.get('tag')

            CPNews.objects.create(
                title=title,
                description=description,
                main_image=main_image,
                news_type=type_,
                author=author,
                link=source_url,
                publish=publish
            )

            last_id = CPNews.objects.last()

            for tag in tags.split(','):
                CPNewsTags.objects.create(
                    news_id=last_id,
                    tag=tag.strip()
                )

            for image in request.FILES.getlist('images'):
                CPNewsImages.objects.create(
                    news_id=last_id,
                    images=image
                )

            messages.add_message(request, messages.SUCCESS, _('Article {} successfully added!').format(last_id.title))
            return redirect(news_page)
        else:
            messages.add_message(request, messages.INFO, form.errors)
            messages.add_message(request, messages.INFO, images_form.errors)
            messages.add_message(request, messages.INFO, tags_form.errors)
            return redirect(news_page)
    else:
        return render(request, 'united/staff/news/add.html', context)
