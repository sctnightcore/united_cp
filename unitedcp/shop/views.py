from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext_lazy as _

from .models import *
from .forms import *


@csrf_protect
@login_required
def shop_main(request):
    values = request.GET
    shop_items = None
    category = None

    if values:
        category = int(values['category'])
        if category:
            shop_items = Shop.filter_item_by_category(category)
    else:
        shop_items = Shop.objects.values().all()
    return render(request, 'default/panel/shop/main.html', {
        'ShopCategories': ShopCategories.objects.values().all(),
        'ShopItems': shop_items,
        'RequestedCategory': category
    })


@login_required
def shop_view_item(request, item):
    purchase = True
    view_item = Shop.objects.values().filter(pk=item).first()
    if view_item['item_sale_ends'] is not None:
        if timezone.now() < view_item['item_sale_ends']:
            # Can't be purchased because sale date ends
            purchase = False

    if view_item['item_amount'] < 1:
        purchase = False
    return render(request, 'default/panel/shop/view_item.html', {
        'ViewedItem': view_item,
        'Purchase': purchase,
        'PageTitle': _('Item view') + ' - \'{}\''.format(view_item['item_name'])
    })
