from django import template
from unitedcp.ragnarok.core import classes
from unitedcp.ragnarok.models import Guild

register = template.Library()


# Credits: [kenik]
@register.simple_tag()
def get_class_name(classid):
    try:
        result = classes[classid]
    except KeyError or AttributeError:
        result = "Undefined (" + str(classid) + ")"
    return result


@register.simple_tag()
def normalize_rate(rate):
    # rate must be int or float
    if type(rate) is int or float:
        value = rate / 100
        return int(value)

    raise TypeError('rate is not int or float!')


@register.simple_tag()
def get_cards_rate(rate):
    # rate must be int or float
    if type(rate) is int or float:
        value = rate / 100 / 100
        return float(value)

    raise TypeError('rate is not int or float!')


@register.simple_tag()
def get_guild_name(guild_id):

    if not guild_id:
        return 'No guild'

    try:
        name = Guild.objects.get(guild_id=guild_id)
    except Guild.DoesNotExist:
        return 'No guild'
    return name.guild_name
