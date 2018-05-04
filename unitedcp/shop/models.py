from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from unitedcp.accounts.models import MasterAccountStorage

ITEM_EXTRA = (
    (0, _('Nothing')),
    (1, _('Name change')),
    (2, _('Account transfer')),
)


def upload_thumbnail(instance, filename):
    return 'shop/thumbnails/{}/{}'.format(instance.item_name, filename)


class ShopCategories(models.Model):
    category_name = models.CharField(max_length=150, verbose_name=_('Category Name'), null=False, blank=False,
                                     default='')

    class Meta:
        db_table = 'cp_shop_categories'
        verbose_name = _('Item Shop Categories')

    def __str__(self):
        return self.category_name


class ShopBundles(models.Model):
    bundle_name = models.CharField(max_length=150, verbose_name=_('Bundle Name'), null=False, blank=False, default='')
    item_id = models.IntegerField(default=0, null=False, verbose_name=_('Item ID'))
    item_amount = models.IntegerField(default=0, null=False, verbose_name=_('Amount'))
    item_extra = models.IntegerField(default=0, null=False, verbose_name=_('Extra services'))

    class Meta:
        db_table = 'cp_shop_bundles'
        verbose_name = _('Shop Bundles')

    def __str__(self):
        return self.bundle_name


class Shop(models.Model):
    item_name = models.CharField(max_length=150, verbose_name=_('Item Name'), null=False, blank=False, default='')
    item_category = models.ForeignKey(ShopCategories, on_delete=models.DO_NOTHING, verbose_name=_('Category'),
                                      null=True)
    item_bundle = models.ForeignKey(ShopBundles, null=True, verbose_name=_('Is bundle'), blank=True,
                                    on_delete=models.DO_NOTHING)
    item_cost = models.FloatField(default=0, null=False, verbose_name=_('Cost'))
    item_discount = models.FloatField(default=0, null=False, verbose_name=_('Discount'),
                                      help_text=_('Discount in percents'))
    item_discount_from = models.DateTimeField(verbose_name=_('Discount date starts'), null=True, blank=True)
    item_discount_until = models.DateTimeField(verbose_name=_('Discount date ends'), null=True, blank=True)
    item_id = models.IntegerField(default=0, null=False, verbose_name=_('Item ID'))
    item_amount = models.IntegerField(default=0, null=False, verbose_name=_('Amount'))
    item_extra = models.IntegerField(default=0, null=False, verbose_name=_('Extra services'), choices=ITEM_EXTRA)
    item_image_thumbnail = models.FileField(max_length=500, default='', verbose_name=_('Thumbnail image'), null=False,
                                            upload_to=upload_thumbnail)
    item_sale_ends = models.DateTimeField(verbose_name=_('Sale date end'), null=True, blank=True)
    item_description = models.TextField(verbose_name=_('Description'), null=False, blank=True,
                                        default='Item description', max_length=5000)

    class Meta:
        db_table = 'cp_shop'
        verbose_name = _('Shop')

    def __str__(self):
        return self.item_name

    @staticmethod
    def filter_item_by_category(category_id):
        ret = []
        filtered_items = Shop.objects.values().filter(item_category=category_id).order_by('-item_name').all()

        for items in filtered_items:
            if items['item_sale_ends']:
                if timezone.now() < items['item_sale_ends']:
                    ret.append(items)
            else:
                ret.append(items)

        return ret or False
