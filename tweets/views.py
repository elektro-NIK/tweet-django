import json
from itertools import chain
from operator import attrgetter

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseForbidden
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import translation
from django.views import View

from tweet_django.settings import TWEETS_PER_PAGE, COMMENTS_PER_PAGE
from tweets.forms import TweetForm, SearchForm, CommentForm
from tweets.models import Tweet, HashTag, Retweet, Like, Comment
from user_profile.models import User, UserFollower


class Index(View):
    @staticmethod
    def get(request):
        return render(request, 'base/base.html', {'title': 'Index'})


class Profile(LoginRequiredMixin, View):
    @staticmethod
    def get(request, username):
        params = {'title': 'User profile'}
        user_profile = User.objects.get(username=username)
        user_follower = UserFollower.objects.get(user=user_profile)
        if user_follower.followers.filter(username=request.user.username).exists():
            params['following'] = True
        else:
            params['following'] = False
        form = TweetForm(initial={'country': 'Global'})
        tweets = Tweet.objects.filter(user=user_profile).filter(is_active=True).order_by('-created')
        retweets = Retweet.objects.filter(user=user_profile).filter(is_active=True).order_by('-created')
        all_tweets = sorted(chain(tweets, retweets), key=attrgetter('created'), reverse=True)
        paginator = Paginator(all_tweets, TWEETS_PER_PAGE)
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
        params['stat'] = {
            'tweets':    len(all_tweets),
            'following': len(User.objects.get(userfollower=user_follower).followers.all()),
            'followers': UserFollower.objects.values_list('count').filter(user=user_profile).get()[0],
        }
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


class TweetView(LoginRequiredMixin, View):
    @staticmethod
    def get(request, tweet_id):
        tweet = Tweet.objects.get(id=tweet_id)
        if tweet.is_active:
            all_comments = sorted(tweet.comments(), key=attrgetter('created'), reverse=True)
            paginator = Paginator(all_comments, COMMENTS_PER_PAGE)
            page = request.GET.get('page')
            try:
                comments = paginator.page(page)
            except PageNotAnInteger:
                comments = paginator.page(1)
            except EmptyPage:
                comments = paginator.page(paginator.num_pages)
            params = {
                'title': 'Tweet',
                'form': CommentForm(),
                'tweet': tweet,
                'comments': comments,
            }
            return render(request, 'tweet.html', params)
        return HttpResponseRedirect(reverse('profile', args=[request.user]))

    @staticmethod
    def post(request, tweet_id):
        form = CommentForm(request.POST)
        if form.is_valid():
            tweet = Tweet.objects.get(id=tweet_id)
            user = User.objects.get(username=request.POST['user'])
            comment = Comment(tweet=tweet, user=user, text=form.cleaned_data['comment'])
            comment.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class NewTweet(LoginRequiredMixin, View):
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
            return HttpResponseRedirect(reverse('profile', args=[user]))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class LikeView(LoginRequiredMixin, View):
    @staticmethod
    def post(request):
        tweet = Tweet.objects.get(id=request.POST['id'])
        user = User.objects.get(username=request.POST['user'])
        like, _ = Like.objects.get_or_create(tweet=tweet)
        if user in like.users.all():
            like.users.remove(user)
        else:
            like.users.add(user)
        return HttpResponse(json.dumps(''), content_type='application/json')


class RetweetView(LoginRequiredMixin, View):
    @staticmethod
    def post(request):
        tweet = Tweet.objects.get(id=request.POST['id'])
        user = User.objects.get(username=request.POST['user'])
        retweet = Retweet(tweet=tweet, user=user)
        retweet.save()
        return HttpResponse(json.dumps(''), content_type='application/json')


class TweetRemove(LoginRequiredMixin, View):
    @staticmethod
    def post(request):
        user = User.objects.get(username=request.user)
        if request.POST['type'] == 'tweet':
            tweet = Tweet.objects.get(id=request.POST['id'])
        elif request.POST['type'] == 'retweet':
            tweet = Retweet.objects.get(id=request.POST['id'])
        if user == tweet.user:
            tweet.is_active = False
            tweet.save()
            return HttpResponse(json.dumps(''), content_type='application/json')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class HashTagPage(LoginRequiredMixin, View):
    @staticmethod
    def get(request, tag):
        try:
            hashtag = HashTag.objects.get(name=tag)
        except HashTag.DoesNotExist:
            hashtag = None
        tweets = hashtag.tweet.all() if hashtag else None
        return render(request, 'hashtag.html', {'title': 'Hashtag', 'tweets': tweets})


class Search(LoginRequiredMixin, View):
    @staticmethod
    def get(request):
        query = request.GET.get('query')
        tweets = Tweet.objects.filter(text__icontains=query).order_by('-created') if query else ' '
        form = SearchForm() if not query else SearchForm(initial={'query': query})
        return render(request, 'search.html', {'title': 'Search', 'search': form, 'tweets': tweets})

    @staticmethod
    def post(request):
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']
            tweets = Tweet.objects.filter(text__icontains=query).order_by('-created')
            return_str = render_to_string('partials/_tweet_wall.html', {'query': query, 'tweets': tweets})
            return HttpResponse(json.dumps(return_str), content_type='application/json')
        else:
            return HttpResponse('')


class SetLang(View):
    @staticmethod
    def get(request, lang):
        lang_code = lang
        next_url = request.META.get('HTTP_REFERER') or '/'
        response = HttpResponseRedirect(next_url)
        translation.activate(lang_code)
        request.session[translation.LANGUAGE_SESSION_KEY] = lang_code
        return response
