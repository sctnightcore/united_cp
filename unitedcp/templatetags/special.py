import time
import codecs
import binascii
import random
import requests

from django import template
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from unitedcp.ragnarok.models import Guild
from unitedcp.staff.news.models import CPNewsTags
from unitedcp.accounts.models import UserProfile
from unitedcp.shop.models import Shop
from ragnarokcp.settings.base import *

register = template.Library()

TAG_SEARCH_URL = '/search/{}/tags'
IMAGE_URL = STATIC_URL + '{}'
ITEMS_ICON_IMAGE_URL = STATIC_URL + 'images/ragnarok/data/items/icons/{}.gif'
ITEMS_COLLECT_IMAGE_URL = STATIC_URL + 'images/ragnarok/data/items/images/{}.png'
JOB_IMAGE_URL = STATIC_URL + 'images/ragnarok/data/jobs/images/{0}/{1}.gif'
MONSTER_IMAGE_URL = STATIC_URL + 'images/ragnarok/data/monsters/{}.gif'
EMBLEMS_IMAGE_URL = STATIC_URL + 'images/ragnarok/data/emblems/{}.bmp'
EMBLEMS_PATH = 'unitedcp' + STATIC_URL + 'images/ragnarok/data/emblems/{}.bmp'


@register.simple_tag()
def get_tags(news_id):
    """
    :param news_id: id of news
    :return: list of tags
    """
    tags_list = ''

    tags = CPNewsTags.objects.values_list('tag').filter(news_id=news_id).all()
    if not tags.exists():
        return 'No tags'

    for tag in tags:
        tag_list = format_html(
            '<a href="{}"><span class="label label-default">{}</span></a> ',
            TAG_SEARCH_URL.format(tag[0]),
            tag[0]
        )
        tags_list += tag_list

    return mark_safe(tags_list)


@register.simple_tag()
def get_donation_coins(account):
    if not account:
        return 0

    coins = UserProfile.objects.values('donation_points').filter(user=account).all()

    if not coins.exists():
        return 0
    return coins[0]['donation_points']


@register.simple_tag()
def get_download_links():
    download_links = ''

    for link in settings.DOWNLOAD:

        if link['image'] == '':
            link['image'] = 'images/dummy.png'

        download_link = format_html(
            '<tr>'
            '<td class="message-from">'
            '<a href="{0}" class="angled-img">'
            '<div class="img">'
            '<img src="{1}" width="80" height="80" alt="">'
            '</div>'
            '</a>'
            '<a href="{0}" class="message-from-name" title="{2}">{2}</a>'
            '<br>'
            '<span class="date">{3}</span>'
            '</td>'
            '<td class="message-description">'
            '<a href="{0}" class="message-description-name" title="Download">{6}</a>'
            '<br>'
            '<div class="message-excerpt">{4}</div>'
            '<br>'
            '<a href="{0}" class="btn btn-sm btn-default"><i class="fa fa-download"></i></a>'
            '</td>'
            '<td class="message-action">'
            '<span class="messages-count">{5}</span>'
            '</td>'
            '</tr>',
            link['link'],
            IMAGE_URL.format(link['image']),
            link['name'],
            link['date'],
            link['description'],
            link['size'],
            link['short_desc']
        )
        download_links += download_link

    return mark_safe(download_links)


@register.simple_tag()
def get_item_image(item_id):
    image = '<img src="{}" alt="">'.format(ITEMS_ICON_IMAGE_URL.format(item_id))
    return mark_safe(image)


@register.simple_tag()
def get_class_image(gender, class_id):
    image = '<img src="{}" alt="Class Image">'.format(JOB_IMAGE_URL.format(gender, class_id))
    return mark_safe(image)


@register.simple_tag()
def get_guild_image(guild_id):
    if not guild_id:
        return ''

    img = str(guild_id)
    try:
        f = open(EMBLEMS_PATH.format(img), 'r+')
        f.close()
        return mark_safe(format_html('<img src="{}" class="guild-flag_emblem"/>', EMBLEMS_IMAGE_URL.format(img)))
    except FileNotFoundError or FileExistsError:
        try:
            guild = Guild.objects.get(guild_id=guild_id)
        except Guild.DoesNotExist:
            return ''
        if guild.emblem_data and guild.emblem_len:
            binary_string = binascii.unhexlify(guild.emblem_data)
            binary_string = codecs.decode(binary_string, "zlib")
            try:
                with open(EMBLEMS_PATH.format(img), 'wb') as f:
                    f.write(binary_string)
                    f.close()
            except FileNotFoundError or FileExistsError:
                return ''
            return mark_safe(format_html('<img src="{}" />', EMBLEMS_IMAGE_URL.format(img)))
        else:
            return ''


@register.simple_tag()
def seconds_to_date(s):
    value = time.strftime('%H:%M:%S', time.gmtime(s))
    return value


@register.simple_tag()
def get_rand_title():
    return random.choice(settings.RANDOM_TITLES)


@register.simple_tag()
def get_discount_price(price, discount):
    discount_price = (price * discount) / 100
    ret = float(price - discount_price)
    return ret or 0


@register.simple_tag()
def get_category_items_count(cat):
    count = Shop.objects.filter(item_category=cat).count()
    return count or 0


@register.simple_tag()
def get_skill_by_api(sk_id):
    value = requests.get('https://www.divine-pride.net/api/database/Skill/{}?apiKey={}'.format(sk_id, 'b442859dbc0f07658b2e4ad74b8e8ba5'))
    r = value.json()
    return r['name']
