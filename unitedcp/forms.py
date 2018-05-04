from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from ragnarokcp.settings.base import *


class LoginForm(forms.Form):
    username = forms.CharField(
        label=_('Login'),
        max_length=150,
        widget=forms.TextInput(
            attrs={
                'placeholder': _('Login'),
                'required': True,
                'class': 'form-control'
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
                'class': 'form-control'
            }
        )
    )


class FastRegisterForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(FastRegisterForm, self).__init__(*args, **kwargs)

    GENDER = (
        ('M', _('Male')),
        ('F', _('Female'))
    )

    email = forms.EmailField(
        label=_('E-Mail'),
        max_length=150,
        widget=forms.EmailInput(
            attrs={
                'placeholder': _('E-Mail'),
                'required': True,
                'class': 'form-control'
            }
        ),
    )

    username = forms.CharField(
        label=_('Login'),
        max_length=MAX_USERNAME_LENGTH,
        min_length=MIN_USERNAME_LENGTH,
        widget=forms.TextInput(
            attrs={
                'placeholder': _('Login'),
                'required': True,
                'class': 'form-control'
            }
        ),
        help_text=_('Your username must be between {} and {} characters'.format(MIN_USERNAME_LENGTH, MAX_USERNAME_LENGTH))
    )

    password = forms.CharField(
        label=_('Password'),
        max_length=MAX_PASSWORD_LENGTH,
        min_length=4,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': _('Password'),
                'required': True,
                'class': 'form-control'
            }
        ),
        help_text=_('Your password must be between {} and {} characters'.format(4, MAX_PASSWORD_LENGTH))
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

    def clean(self):
        cleaned_data = super(FastRegisterForm, self).clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if len(username) < MIN_USERNAME_LENGTH or len(username) > MAX_USERNAME_LENGTH:
            raise ValidationError(_("Your username must be between {min_length} and {max_length} characters."),
                                  code='wrong_username_Length',
                                  params={'min_length': MIN_USERNAME_LENGTH, 'max_length': MAX_USERNAME_LENGTH})

        return cleaned_data


class RegisterForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields['rules'].required = False

    email = forms.EmailField(
        label=_('E-Mail'),
        max_length=150,
        widget=forms.EmailInput(
            attrs={
                'placeholder': _('E-Mail'),
                'required': True,
                'class': 'form-control'
            }
        ),
    )

    username = forms.CharField(
        label=_('Login'),
        max_length=MAX_USERNAME_LENGTH,
        min_length=MIN_USERNAME_LENGTH,
        widget=forms.TextInput(
            attrs={
                'placeholder': _('Login'),
                'required': True,
                'class': 'form-control'
            }
        ),
        help_text=_('Your username must be between {} and {} characters'.format(MIN_USERNAME_LENGTH, MAX_USERNAME_LENGTH))
    )

    password = forms.CharField(
        label=_('Password'),
        max_length=MAX_PASSWORD_LENGTH,
        min_length=4,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': _('Password'),
                'required': True,
                'class': 'form-control'
            }
        ),
        help_text=_('Your password must be between {} and {} characters'.format(4, MAX_PASSWORD_LENGTH))
    )

    confirm_password = forms.CharField(
        label=_('Confirm password'),
        max_length=MAX_PASSWORD_LENGTH,
        min_length=4,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': _('Confirm password'),
                'required': True,
                'class': 'form-control'
            }
        ),
        help_text=_('Confirm password.')
    )

    rules = forms.CharField(
        label=_('Rules'),
        help_text=_('I comply with rules'),
        widget=forms.CheckboxInput(
            attrs={
                'title': 'I comply with rules',
                'id': 'toggleButton11'
            },
        )
    )

    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        rules = cleaned_data.get('rules')

        if rules == 'False':
            raise ValidationError(_("You must accept server rules"), code='accept_rules')

        if len(username) < MIN_USERNAME_LENGTH or len(username) > MAX_USERNAME_LENGTH:
            raise ValidationError(_("Your username must be between {min_length} and {max_length} characters."),
                                  code='wrong_username_Length',
                                  params={'min_length': MIN_USERNAME_LENGTH, 'max_length': MAX_USERNAME_LENGTH})

        if password != confirm_password:
            raise ValidationError(_("Password doesn\'t match!"), code='password_doesnt_match')
        return cleaned_data


class UserPasswordResetForm(forms.Form):
    email = forms.EmailField(
        label=_('E-Mail'),
        max_length=150,
        widget=forms.TextInput(
            attrs={
                'placeholder': _('E-Mail'),
                'required': True,
                'class': 'form-control'
            }
        )
    )
