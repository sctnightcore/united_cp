from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import (User, AbstractBaseUser)

from unitedcp.ragnarok.models import Char
from unitedcp.shop.models import Shop


class UserVerification(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    key = models.CharField(max_length=255, null=False, default='', verbose_name=_('Verification Key'), unique=True)
    verification_date = models.DateTimeField(default=timezone.now, verbose_name=_('Date'))
    key_expires = models.DateTimeField()
    action = models.IntegerField(default=0, verbose_name=_('Action'), null=False)
    new_value = models.CharField(max_length=255, verbose_name=_('Value'), null=False, default='')

    class Meta:
        verbose_name = _('User verification')
        db_table = 'cp_user_verification'

    def __str__(self):
        return self.user.username


class CPHighPeak(models.Model):
    num_users = models.IntegerField()
    peak_date = models.CharField(max_length=255, default='')

    class Meta:
        db_table = 'cp_highest_peak'

class PanelLogs(models.Model):
    user = models.IntegerField(default=0, null=True, blank=True)
    action = models.CharField(max_length=500, default='', null=False)
    code = models.IntegerField(default=0, null=True, blank=True)
    date = models.DateTimeField(default=timezone.now, null=False)
    ip = models.GenericIPAddressField(default='', null=False)
    agent = models.CharField(max_length=1000, default='', null=False)
    device = models.CharField(max_length=1000, default='', null=False)
    os = models.CharField(max_length=1000, default='', null=False)

    class Meta:
        verbose_name = _('Panel Logs')
        db_table = 'cp_panel_log'

    def __str__(self):
        return '#{} -{}'.format(self.user, self.date)

    def get_agent(self):
        user_agent = '{} {} {}'.format(self.os, self.device, self.agent)
        return user_agent.strip()


class UserRewards(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    reward_id = models.IntegerField(default=0, null=False)
    reward_amount = models.IntegerField(default=0, null=False)

    class Meta:
        verbose_name = _('User Rewards')
        db_table = 'cp_user_rewards'

    def __str__(self):
        return self.user.username


class UserCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    item = models.ForeignKey(Shop, on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name = _('User Cart')
        db_table = 'cp_user_cart'

    def __str__(self):
        return self.user.username
