from django import forms
from unitedcp.staff.news.models import *


class AddNewsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AddNewsForm, self).__init__(*args, **kwargs)
        self.fields['link'].required = False
        self.fields['description'].required = False

    class Meta:
        model = CPNews
        fields = {'title', 'description', 'main_image', 'news_type', 'author', 'link', 'publish'}

        widgets = {
            'title': forms.TextInput(
                attrs={
                    'required': True,
                    'placeholder': 'News title...',
                    'label': 'Title'
                },
            ),
            'description': forms.Textarea(
                attrs={
                    'required': False,
                },
            ),
            'main_image': forms.FileInput(
                attrs={
                    'required': False,
                },
            ),
            'news_type': forms.Select(
                attrs={
                    'required': False,
                },
                choices=CPNews.NEWS_TYPE
            ),
            'author': forms.TextInput(
                attrs={
                    'required': False,
                    'placeholder': 'News author...',
                },
            ),
            'link': forms.URLInput(
                attrs={
                    'required': False,
                    'placeholder': 'Source URL',
                },
            ),
            'publish': forms.CheckboxInput(
                attrs={
                    'required': False,
                },
            ),
        }

    def __str__(self):
        return self.title


class AddNewsImagesForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AddNewsImagesForm, self).__init__(*args, **kwargs)
        self.fields['images'].required = False

    class Meta:
        model = CPNewsImages
        fields = {'images'}

        widgets = {
            'images': forms.ClearableFileInput(
                attrs={
                    'required': False,
                    'multiple': True
                },
            ),
        }


class AddNewsTagsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AddNewsTagsForm, self).__init__(*args, **kwargs)
        self.fields['tag'].required = False

    class Meta:
        model = CPNewsTags
        fields = {'tag'}

        widgets = {
            'tag': forms.TextInput(
                attrs={
                    'required': False,
                    'placeholder': 'Type tags separated by commas...',
                },
            ),
        }
