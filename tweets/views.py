import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.views import View

from tweet_django.settings import TWEETS_PER_PAGE
from tweets.forms import TweetForm, SearchForm
from tweets.models import Tweet, HashTag
from user_profile.models import User, UserFollower


class Index(View):
    @staticmethod
    def get(request):
        return render(request, 'base.html', {'name': 'World'})


class Profile(LoginRequiredMixin, View):
    @staticmethod
    def get(request, username):
        params = {}
        user_profile = User.objects.get(username=username)
        user_follower = UserFollower.objects.get(user=user_profile)
        if user_follower.followers.filter(username=request.user.username).exists():
            params['following'] = True
        else:
            params['following'] = False
        form = TweetForm(initial={'country': 'Global'})
        search_form = SearchForm()
        tweets = Tweet.objects.filter(user=user_profile).order_by('-created')
        paginator = Paginator(tweets, TWEETS_PER_PAGE)
        page = request.GET.get('page')
        try:
            tweets = paginator.page(page)
        except PageNotAnInteger:
            tweets = paginator.page(1)
        except EmptyPage:
            tweets = paginator.page(paginator.num_pages)
        params['tweets'] = tweets
        params['profile'] = user_profile
        params['form'] = form
        params['search'] = search_form
        return render(request, 'profile.html', params)

    @staticmethod
    def post(request, username):
        follow = request.POST['follow']
        user = User.objects.get(username=request.user.username)
        user_profile = User.objects.get(username=username)
        user_follower, _ = UserFollower.objects.get_or_create(user=user_profile)
        if follow == 'true':
            # follow
            user_follower.count += 1
            user_follower.save()
            user_follower.followers.add(user)
        else:
            # unfollow
            user_follower.count -= 1
            user_follower.save()
            user_follower.followers.remove(user)
        return HttpResponse(json.dumps(''), content_type='application/json')


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


class Search(View):
    @staticmethod
    def get(request):
        form = SearchForm()
        return render(request, 'search.html', {'search': form})

    @staticmethod
    def post(request):
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']
            tweets = Tweet.objects.filter(text__icontains=query)
            return_str = render_to_string('partials/_tweet_search.html', {'query': query, 'tweets': tweets})
            return HttpResponse(json.dumps(return_str), content_type='application/json')
        else:
            return HttpResponseRedirect('/search/')
