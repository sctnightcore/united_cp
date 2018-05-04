from django import forms
from .models import UserAnnouncements, UserAnnouncementsComments


class UserAnnouncementsForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(UserAnnouncementsForm, self).__init__(*args, **kwargs)
        self.fields['message'].required = False
        self.fields['announce_type'].label = 'Announcement type'
        self.fields['title'].label = 'Title'

    class Meta:
        model = UserAnnouncements
        fields = {'title', 'announce_type', 'message'}

        widgets = {
            'title': forms.TextInput(
                attrs={
                    'required': True,
                    'placeholder': 'Title',
                },
            ),
            'message': forms.Textarea(
                attrs={
                    'required': False,
                    'placeholder': 'Message',
                },
            ),
            'announce_type': forms.Select(
                attrs={
                    'required': True,
                },
                choices=UserAnnouncements.ANNOUNCEMENTS_TYPE
            )
        }

    def __str__(self):
        return self.title


class UserAnnouncementsCommentForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(UserAnnouncementsCommentForm, self).__init__(*args, **kwargs)
        self.fields['message'].required = False

    class Meta:
        model = UserAnnouncementsComments
        fields = {'message'}

        widgets = {
            'message': forms.Textarea(
                attrs={
                    'required': False,
                    'placeholder': 'Message',
                    'label': 'Message'
                },
            ),
        }