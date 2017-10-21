from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _


def _input_field(placeholder):
        return forms.TextInput(attrs={'class': 'form-control', 'placeholder': _(placeholder)})


def _email_field(placeholder='Email'):
    return forms.EmailInput(attrs={'class': 'form-control', 'placeholder': _(placeholder)})


def _password_field(placeholder='Password'):
    return forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': _(placeholder)})


class SignupForm(forms.Form):
    username = forms.CharField(max_length=30, widget=_input_field('Username'))
    first_name = forms.CharField(max_length=30, required=False, widget=_input_field('First name'))
    last_name = forms.CharField(max_length=30, required=False, widget=_input_field('Last name'))
    email = forms.EmailField(widget=_email_field())
    password = forms.CharField(widget=_password_field())

    def clean_username(self):
        if User.objects.filter(username=self.cleaned_data['username']):
            raise forms.ValidationError('This username is already in use')
        return self.cleaned_data['username']

    def clean_email(self):
        if User.objects.filter(email=self.cleaned_data['email']):
            raise forms.ValidationError('This email is already in use')
        return self.cleaned_data['email']
