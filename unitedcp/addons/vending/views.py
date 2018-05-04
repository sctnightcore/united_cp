from django.shortcuts import render, redirect
from unitedcp.ragnarok.models import (Vendings, VendingItems)


def vending_index(request):
    return render(request, 'vending/main.html')


def view_vendor_byid(request, vending_id):
    if not vending_id:
        return redirect(vending_index)

    vending_items = VendingItems.objects.values('cartinventory_id__nameid__name_japanese', 'cartinventory_id__refine', 'cartinventory_id__card0__name_japanese',
                                                'cartinventory_id__card1__name_japanese', 'cartinventory_id__card2__name_japanese',
                                                'cartinventory_id__card3__name_japanese', 'price', 'amount', 'cartinventory_id__nameid__slots', 'vending_id__title',
                                                'vending_id__char_id__name', 'vending_id__map', 'vending_id__x', 'vending_id__y', 'cartinventory_id__nameid').filter(
        vending_id=vending_id).all()

    return render(request, 'vending/view.html', {
        'VendingItems': vending_items,
    })
