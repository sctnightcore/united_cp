import os
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from unitedcp.models import (PanelLogs, UserRewards)
from ragnarokcp import settings


def guide_upload(instance, filename):
    return 'guides/images/{0}/{1}'.format(instance.title, filename)


def main_image_validation(file):
    ext = os.path.splitext(file.name)[1]
    if ext not in settings.VALID_EXTENTIONS:
        raise ValidationError(_('File not supported!'), code='file_not_supported')

    if file._size > settings.GUIDE_MAX_IMAGE_SIZE:
        raise ValidationError(_('File size too big'), code='size_too_big')


GUIDE_CATEGORIES = (
    ('quest_guide', 'Quest Guide'),
    ('class_guide', 'Class Guide'),
    ('other', 'Other')
)


class UserGuide(models.Model):
    title = models.CharField(max_length=50, default='', null=False)
    category = models.CharField(max_length=30, default='', null=False, choices=GUIDE_CATEGORIES)
    on_moderation = models.BooleanField(default=True, null=False)
    description = models.TextField(default='', null=False, blank=True)
    main_image = models.ImageField(verbose_name='Main Image', upload_to=guide_upload, default='', validators=[main_image_validation])
    date = models.DateTimeField(null=False, default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    class Meta:
        db_table = 'cp_user_guides'

    def __str__(self):
        return self.title

    def apply_guide(self, moderator, reward_id, reward_amount, ip):
        PanelLogs.objects.create(action='Guide {} applied by {}'.format(self.title, moderator), user=self.user.id, code=10, ip=ip)
        UserRewards.objects.create(user=self.user, reward_id=reward_id, reward_amount=reward_amount)
        self.on_moderation = False
        self.save()


class UserGuideReward(models.Model):
    category = models.CharField(max_length=30, default='', null=False, choices=GUIDE_CATEGORIES)
    reward_id = models.IntegerField(default=0, null=False)
    reward_amount = models.IntegerField(default=0, null=False)

    def __str__(self):
        return '{} > {}'.format(self.category, self.reward_id)

    class Meta:
        db_table = 'cp_user_guide_rewards'


class UserGuideTag(models.Model):
    guide = models.ForeignKey(UserGuide, on_delete=models.DO_NOTHING)
    tag = models.CharField(max_length=100, null=False, default='')

    class Meta:
        db_table = 'cp_user_guide_tags'

    def __str__(self):
        return self.guide.title
