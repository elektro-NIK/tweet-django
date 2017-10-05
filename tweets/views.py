from django.shortcuts import render
from django.views import View

from tweets.models import Tweet
from user_profile.models import User


class Index(View):
    def get(self, request):
        return render(request, 'base.html', {'name': 'World'})


class Profile(View):
    def get(self, request, username):
        user = User.objects.get(username=username)
        tweets = Tweet.objects.filter(user=user)
        return render(request, 'profile.html', {
            'user': user,
            'tweets': tweets,
        })
