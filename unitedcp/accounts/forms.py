from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from .models import UserProfile, User


class UserChangeEmailForm(forms.Form):
    new_email = forms.CharField(
        label=_('New E-Mail'),
        max_length=150,
        widget=forms.EmailInput(
            attrs={
                'placeholder': _('New E-Mail'),
                'required': True,
                'class': 'form-control'
            }
        )
    )


class UserChangePasswordForm(forms.Form):
    old_password = forms.CharField(
        label=_('Old password'),
        max_length=150,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': _('Old password'),
                'required': True,
                'class': 'form-control'
            }
        )
    )

    new_password = forms.CharField(
        label=_('New password'),
        max_length=150,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': _('New password'),
                'required': True,
                'class': 'form-control'
            }
        )
    )


class UserProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.fields['phone'].required = False
        self.fields['user_avatar'].required = False
        self.fields['viewable'].required = False
        self.fields['receive_notifications'].required = False

    class Meta:
        model = UserProfile
        fields = {
            'viewable',
            'user_avatar',
            'phone',
            'receive_notifications'
        }

        widgets = {
            'viewable': forms.CheckboxInput(
                attrs={
                    'required': False
                },
            ),
            'user_avatar': forms.FileInput(
                attrs={
                    'class': 'form-control form-control-line',
                    'required': False
                }
            ),
            'phone': forms.TextInput(
                attrs={
                    'class': 'form-control form-control-line',
                    'required': False
                }
            ),
            'receive_notifications': forms.CheckboxInput(
                attrs={
                    'required': False
                }
            )
        }

    def clean(self):
        phone = self.cleaned_data.get('phone')
        notifications = self.cleaned_data.get('receive_notifications')

        if notifications == 'True' and phone == '':
            raise ValidationError(_('You can\'t enable notifications if you don\'t input phone number'), code='notifications_failed')
        return self.cleaned_data


class MainUserForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(MainUserForm, self).__init__(*args, **kwargs)
        self.fields['password'].required = False

    class Meta:
        model = User

        fields = {
            'first_name',
            'last_name',
            'email',
            'password'
        }

        widgets = {
            'first_name': forms.TextInput(
                attrs={
                    'class': 'form-control form-control-line',
                    'required': False
                }
            ),
            'last_name': forms.TextInput(
                attrs={
                    'class': 'form-control form-control-line',
                    'required': False
                }
            ),
            'email': forms.EmailInput(
                attrs={
                    'class': 'form-control form-control-line',
                    'required': False
                }
            ),
            'password': forms.PasswordInput(
                attrs={
                    'class': 'form-control form-control-line',
                    'required': False
                }
            ),
        }


class PromoPageForm(forms.Form):
    code = forms.CharField(
        label=_('Промо-код'),
        max_length=150,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': _('Введите промо-код'),
                'required': True,
                'class': 'form-control'
            }
        )
    )