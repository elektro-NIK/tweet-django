from django import forms


class TweetForm(forms.Form):
    text = forms.CharField(
        widget=forms.Textarea(
            attrs={'rows': 1, 'cols': 85, 'class': 'form-control post-tweet', 'placeholder': 'New tweet'}
        ),
        max_length=140
    )
    country = forms.CharField(required=False, widget=forms.HiddenInput())


class SearchForm(forms.Form):
    query = forms.CharField(
        label='Enter a keyword to search for',
        widget=forms.TextInput(attrs={'class': 'search-query'})
    )
