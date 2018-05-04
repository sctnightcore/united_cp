from django.db import models
from django.utils.translation import ugettext_lazy as _


def upload_news(instance, filename):
    return 'news/main_images/{0}/{1}'.format(instance.title, filename)


def upload_images(instance, filename):
    return 'news/images/{0}/{1}'.format(instance.news_id.title, filename)


class CPNews(models.Model):
    NEWS_TYPE = (
        ('Patch Note', _('Patch Note')),
        ('Event', _('Event')),
        ('News', _('News'))
    )

    title = models.CharField(max_length=150, null=False, default='', verbose_name=_('Title'))
    date = models.DateTimeField(verbose_name=_('Date'), auto_now=True)
    description = models.TextField(verbose_name=_('Description'), max_length=10000, null=False, default='')
    main_image = models.ImageField(verbose_name=_('Main Image'), upload_to=upload_news, default='')
    news_type = models.CharField(max_length=20, choices=NEWS_TYPE, default='Patch Note', verbose_name=_('Type'))
    author = models.CharField(max_length=150, null=False, default='', verbose_name=_('Author'))
    link = models.URLField(verbose_name=_('Source url'), default='', null=False)
    publish = models.BooleanField(verbose_name=_('Publish'), default=False)

    class Meta:
        db_table = 'cp_news'

    def __str__(self):
        if not self.author:
            self.author = _('No author')
        return '{} by {}'.format(self.title, self.author)


class CPNewsImages(models.Model):
    news_id = models.ForeignKey(CPNews, on_delete=models.CASCADE)
    images = models.ImageField(verbose_name=_('Images'), upload_to=upload_images, default='')

    class Meta:
        db_table = 'cp_news_images'


class CPNewsTags(models.Model):
    news_id = models.ForeignKey(CPNews, on_delete=models.CASCADE)
    tag = models.CharField(max_length=150, null=False, default='', verbose_name=_('Tags'))

    class Meta:
        db_table = 'cp_news_tags'