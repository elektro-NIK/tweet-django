from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View

from tweets.forms import TweetForm
from tweets.models import Tweet, HashTag
from user_profile.models import User


class Index(View):
    @staticmethod
    def get(request):
        return render(request, 'base.html', {'name': 'World'})


class Profile(View):
    @staticmethod
    def get(request, username):
        user = User.objects.get(username=username)
        tweets = Tweet.objects.filter(user=user)
        return render(request, 'profile.html', {
            'user':   user,
            'tweets': tweets,
            'form':   TweetForm(),
        })


class PostTweet(View):
    @staticmethod
    def post(request, username):
        form = TweetForm(request.POST)
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


class HashTagPage(View):
    @staticmethod
    def get(request, tag):
        hashtag = HashTag.objects.get(name=tag)
        return render(request, 'hashtag.html', {'tweets': hashtag.tweet})
