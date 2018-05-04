from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from unitedcp.guides.models import (UserGuide, UserGuideTag)


class GuideSearchForm(forms.Form):
    guide_search = forms.CharField(
        max_length=100,
        label='Search',
        widget=forms.TextInput(
            attrs={
                'placeholder': _('Search guide'),
                'class': 'form-control',
                'required': True,
                'min-length': 3,
            }
        )
    )

    def clean_guide_search(self):
        word = self.cleaned_data.get('guide_search')

        if len(word) < 3:
            raise ValidationError(_('Minimum search word length is 3'), code='search_too_short')

        return word


class GuideAddForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(GuideAddForm, self).__init__(*args, **kwargs)
        self.fields['main_image'].required = False

    class Meta:
        model = UserGuide

        fields = {'title', 'category', 'description', 'main_image'}

        widgets = {
            'title': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'required': True,
                    'placeholder': _('Title'),
                    'data-emojiable': True
                }
            ),
            'category': forms.Select(
                attrs={
                    'class': 'form-control',
                    'required': True,
                }
            ),
            'description': forms.Textarea(
                attrs={
                    'required': False
                }
            ),
            'main_image': forms.FileInput()
        }

    def clean_description(self):
        description = self.cleaned_data.get('description')

        if not description:
            raise ValidationError(_('Description not found'), code='desc_not_found')

        if len(description) < 200:
            raise ValidationError(_('Desciption too short'), code='desc_too_short')
        return description

    def clean_title(self):
        title = self.cleaned_data.get('title')

        if len(title) < 5:
            raise ValidationError(_('Title too short'), code='title_too_short')
        return title


class GuideAddTagForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(GuideAddTagForm, self).__init__(*args, **kwargs)
        self.fields['tag'].value = ''

    class Meta:
        model = UserGuideTag
        fields = ['tag']

        widgets = {
            'tag': forms.TextInput(
                attrs={
                    'required': True,
                    'class': 'form-control',
                    'placeholder': _('Type tags separated by commas...')
                }
            )
        }

    def clean_tag(self):
        tag = self.cleaned_data.get('tag')

        if len(tag) < 3:
            raise ValidationError(_('Tag too short'), code='tag_too_short')
        return tag
