from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _


class DonationsLog(models.Model):
    use_in_migrations = True

    payment_id = models.CharField(verbose_name='Payment ID', null=False, default='', max_length=1000)
    finished = models.BooleanField(default=False, verbose_name='Finished', null=False)
    log = models.CharField(verbose_name='Log', null=False, default='', max_length=1000)
    error_code = models.IntegerField(verbose_name='Error Code', null=False, default=0)
    payment_system = models.CharField(verbose_name='Payment System', null=False, default='', max_length=1000)
    date = models.DateTimeField(verbose_name='Date', auto_now=True)
    donate_value = models.FloatField(verbose_name='Donation Value', default=0, null=False)
    points_value = models.FloatField(verbose_name='Points Value', default=0, null=False)
    user = models.IntegerField(verbose_name='AccountID', default=0, null=False)

    class Meta:
        db_table = 'cp_donatelog'
        verbose_name = _('Donations')

    def __str__(self):
        return '[{}]: #{}, finished ({}) '.format(self.payment_system, self.payment_id, str(self.finished))
