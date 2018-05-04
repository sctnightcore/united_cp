from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


class UserAnnouncements(models.Model):
    ANNOUNCEMENTS_TYPE = (
        (_('Purchase'), _('Purchase')),
        (_('Sell'), _('Sell')),
        (_('Exchange'), _('Exchange')),
        (_('Other'), _('Other'))
    )

    user = models.IntegerField(default=0, null=True, blank=True)
    title = models.CharField(max_length=120, default='', null=True, blank=True)
    announce_type = models.CharField(max_length=20, choices=ANNOUNCEMENTS_TYPE, default=1, verbose_name=_('Type'))
    main_character = models.CharField(max_length=36, default='Char', null=True, blank=True)
    message = models.TextField(max_length=2000, default='', null=True, blank=True)
    announce_date = models.DateTimeField(verbose_name=_('Created date'), default=timezone.now, null=True, blank=True)
    updated_date = models.DateTimeField(verbose_name=_('Updated date'), default=timezone.now, null=True, blank=True)

    class Meta:
        db_table = 'cp_user_announcements'

    def __str__(self):
        return self.title


class UserAnnouncementsComments(models.Model):
    user = models.IntegerField(default=0, null=True, blank=True)
    announce = models.ForeignKey(UserAnnouncements, on_delete=models.DO_NOTHING)
    character = models.CharField(max_length=36, default='Char', null=True, blank=True)
    message = models.TextField(max_length=2000, default='', null=True, blank=True)
    comment_date = models.DateTimeField(verbose_name=_('Date'), default=timezone.now, null=True, blank=True)

    class Meta:
        db_table = 'cp_user_comments'

    def __str__(self):
        return '{} - {}'.format(self.announce.title, self.character)
