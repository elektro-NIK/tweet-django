from django import forms
from django.utils.translation import ugettext_lazy as _


class SignupForm(forms.Form):
    username = forms.CharField(max_length=30, label=_('Username'))
    first_name = forms.CharField(max_length=30, label=_('First name'))
    last_name = forms.CharField(max_length=30, label=_('Last name'))
    email = forms.EmailField(label=_('Email'))
    password = forms.CharField(widget=forms.PasswordInput, label=_('Password'))
