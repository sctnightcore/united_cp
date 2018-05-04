from django import template
from django.db.models import Sum

from unitedcp.ragnarok.models import Char, AccRegNumDb

register = template.Library()


@register.simple_tag()
def characters_amount(account_id):

    if not account_id:
        return None

    characters = Char.objects.filter(account_id=account_id).count()
    return characters or 0


@register.simple_tag()
def cash_amount(account_id):

    if not account_id:
        return None

    cash_points = AccRegNumDb.objects.values().filter(account_id=account_id, key='#CASHPOINTS').aggregate(Sum('value'))
    if cash_points['value__sum'] is None:
        cash_points['value__sum'] = 0

    return cash_points['value__sum']


@register.simple_tag()
def zeny_amount(account_id):

    if not account_id:
        return None

    zeny = Char.objects.values().filter(account_id=account_id).aggregate(Sum('zeny'))
    if zeny['zeny__sum'] is None:
        zeny['zeny__sum'] = 0

    return zeny['zeny__sum']
