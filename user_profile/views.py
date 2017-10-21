from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View

from user_profile.forms import SignupForm
from user_profile.models import UserFollower


class UserRedirect(View):
    @staticmethod
    def get(request):
        return HttpResponseRedirect('/user/{}/'.format(request.user.username))


class MostFollowedUsers(View):
    @staticmethod
    def get(request):
        user_followers = UserFollower.objects.order_by('-count')[:10]
        return render(request, 'users.html', {'user_followers': user_followers})


class Logout(View):
    @staticmethod
    def get(request):
        logout(request)
        try:
            url = request.GET['next']
        except KeyError:
            url = '/'
        return HttpResponseRedirect(url)


class Signup(View):
    @staticmethod
    def get(request):
        form = SignupForm()
        return render(request, 'signup.html', {'form': form})

    @staticmethod
    def post(request):
        form = SignupForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name']
            )
            UserFollower.create(user).save()
            try:
                next_url = request.GET['next']
            except KeyError:
                next_url = '/user/{}'.format(user.username)
            return HttpResponseRedirect('/login/?next={}'.format(next_url))
        return render(request, 'signup.html', {'form': form})
