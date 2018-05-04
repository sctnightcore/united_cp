from django import template
from django.utils.safestring import mark_safe

from ragnarokcp.settings.base import *
from unitedcp import gat

register = template.Library()

MAP_IMAGE_URL = STATIC_URL + 'images/ragnarok/data/maps/{}.png'
GAT_IMAGE_RUL = os.path.join(BASE_DIR, 'unitedcp/static/images/ragnarok/data/maps/{}.gat')


@register.simple_tag()
def vendor_map(map_, x, y):
    try:
        fh = open(GAT_IMAGE_RUL.format(map_), 'rb')
        g = gat.Gat(fh)
        fh.close()
        g.draw_map(x, y, False, 2, map_)

        image = '<img src="{}" class="img-responsive" alt="map">'.format(MAP_IMAGE_URL.format(map_))
        return mark_safe(image)
    except FileExistsError or FileNotFoundError:
        return 'Локация не найдена.'
