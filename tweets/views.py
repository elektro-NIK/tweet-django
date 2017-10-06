from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View

from tweets.forms import TweetForm
from tweets.models import Tweet, HashTag
from user_profile.models import User


class Index(View):
    def get(self, request):
        return render(request, 'base.html', {'name': 'World'})


class Profile(View):
    def get(self, request, username):
        user = User.objects.get(username=username)
        tweets = Tweet.objects.filter(user=user)
        return render(request, 'profile.html', {
            'user':   user,
            'tweets': tweets,
            'form':   TweetForm(),
        })


class PostTweet(View):
    def post(self, request, username):
        form = TweetForm(request.POST)
        #form.is_valid()
        #raise form
        if form.is_valid():
            user = User.objects.get(username=username)
            tweet = Tweet(
                text=form.cleaned_data['text'],
                user=user,
                country=form.cleaned_data['country'],
            )
            tweet.save()
            words = form.cleaned_data['text'].split(' ')
            for word in words:
                if word[0] == '#':
                    tag, created = HashTag.objects.get_or_create(name=word[1:])
                    tag.tweet.add(tweet)
            return HttpResponseRedirect('/user/{}/'.format(username))
        return render(request, 'profile.html', {'form': form})

