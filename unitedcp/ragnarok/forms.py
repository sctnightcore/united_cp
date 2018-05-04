from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from ragnarokcp.settings.base import *


class GameRegisterForm(forms.Form):
    GENDER = (
        ('M', _('Male')),
        ('F', _('Female'))
    )

    username = forms.CharField(
        label=_('Login'),
        max_length=150,
        widget=forms.TextInput(
            attrs={
                'placeholder': _('Login'),
                'required': True,
                'class': 'form-control form-control-line'
            }
        )
    )

    password = forms.CharField(
        label=_('Password'),
        max_length=150,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': _('Password'),
                'required': True,
                'class': 'form-control form-control-line'
            }
        )
    )

    gender = forms.CharField(
        label=_('Gender'),
        max_length=100,
        widget=forms.Select(
            attrs={
                'title': _('Select gender'),
                'required': True,
                'class': 'form-control form-control-line'
            },
            choices=GENDER
        )
    )

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if len(username) < MIN_USERNAME_LENGTH or len(username) > MAX_USERNAME_LENGTH:
            raise ValidationError(_("Your username must be between {min_length} and {max_length} characters."),
                                  code='username_too_short',
                                  params={'min_length': MIN_USERNAME_LENGTH, 'max_length': MAX_USERNAME_LENGTH})
        return username

    def clean_password(self):
        password = self.cleaned_data.get('password')

        if len(password) > MAX_PASSWORD_LENGTH:
            raise ValidationError(_("Use {max_length} characters or fewer for username."),
                                  code='password_too_long',
                                  params={'max_length': MIN_PASSWORD_UPPERCASE})
        return password


class GameChangePasswordForm(forms.Form):

    new_password = forms.CharField(
        label='New password',
        max_length=150,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': _('New password'),
                'required': True,
                'class': 'form-control form-control-line'
            }
        )
    )


class SetMasterAccountForm(forms.Form):

    username = forms.CharField(
        label=_('Login'),
        max_length=150,
        widget=forms.TextInput(
            attrs={
                'placeholder': _('Login'),
                'required': True,
                'class': 'form-control form-control-line'
            }
        )
    )

    password = forms.CharField(
        label=_('Password'),
        max_length=150,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': _('Password'),
                'required': True,
                'class': 'form-control form-control-line'
            }
        )
    )

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if len(username) < MIN_USERNAME_LENGTH or len(username) > MAX_USERNAME_LENGTH:
            raise ValidationError(_("Your username must be between {min_length} and {max_length} characters."),
                                  code='username_too_short',
                                  params={'min_length': MIN_USERNAME_LENGTH, 'max_length': MAX_USERNAME_LENGTH})
        return username

    def clean_password(self):
        password = self.cleaned_data.get('password')

        if len(password) > MAX_PASSWORD_LENGTH:
            raise ValidationError(_("Use {max_length} characters or fewer for username."),
                                  code='password_too_long',
                                  params={'max_length': MIN_PASSWORD_UPPERCASE})
        return password
