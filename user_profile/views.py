from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View

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
