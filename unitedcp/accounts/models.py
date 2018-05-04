from django.db import models
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db.models.signals import pre_init
from django.utils.translation import ugettext_lazy as _


def upload_avatar(instance, filename):
    return 'avatars/{0}/{1}'.format(instance.user.username, filename)


class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    donation_points = models.IntegerField(verbose_name=_('Donation Points'), null=False, default=0)
    ro_character = models.IntegerField(verbose_name=_('Character ID'), null=False, default=0)
    viewable = models.BooleanField(default=False, null=False, verbose_name=_('Viewable Profile'))
    user_avatar = models.FileField(verbose_name=_('Avatar'), max_length=500, upload_to=upload_avatar)
    phone = models.CharField(verbose_name=_('Phone'), max_length=100, default='', null=False)
    receive_notifications = models.BooleanField(default=False, null=False, verbose_name=_('Receive Notifications'))

    class Meta:
        db_table = 'cp_user_profile'

    def __str__(self):
        return self.user.username

    def get_main_character(self):
        return self.ro_character

    def set_main_character(self, new_id):
        self.ro_character = new_id
        self.save()

    def del_main_character(self):
        self.ro_character = 0
        self.save()

    def can_view(self):
        return self.viewable


@receiver(pre_init, sender=User)
def create_user_profile(sender, instance=None, **kwargs):
    if instance:
        UserProfile.objects.create(user=instance)


class MasterAccountStorage(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, default=0)
class PromoCodes(models.Model):

    code = models.CharField(max_length=128, null=False, default='')
    reward = models.IntegerField()
    amount = models.IntegerField()

    class Meta:
        db_table = 'cp_promo_codes'
