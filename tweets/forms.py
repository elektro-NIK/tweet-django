from django import forms


class TweetForm(forms.Form):
    text = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 1, 'cols': 85}),
        max_length=140,
        help_text='Enter your tweet')
    country = forms.CharField(required=False, widget=forms.HiddenInput())
