"""tweet_django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth.views import LoginView

from tweets.views import *
from user_profile.views import UserRedirect, MostFollowedUsers, Logout, Signup

urlpatterns = [
    url(r'^$', Index.as_view(),                                             name='index'),
    url(r'^user/(\w+)/$', Profile.as_view(),                                name='profile'),
    url(r'^user/(\w+)/newtweet/$', NewTweet.as_view(),                      name='new_post'),
    url(r'^tweet/remove/$', TweetRemove.as_view(),                           name='remove_tweet'),
    url(r'^tweet/([0-9]+)/$', TweetView.as_view(),                          name='tweet'),
    url(r'^like/$', LikeView.as_view(),                                     name='like'),
    url(r'^retweet/$', RetweetView.as_view(),                               name='retweet'),
    url(r'^hashtag/(\w+)/$', HashTagPage.as_view(),                         name='hashtag'),
    url(r'^search/$', Search.as_view(),                                     name='search'),
    url(r'^signup/$', Signup.as_view(),                                     name='signup'),
    url(r'^login/$', LoginView.as_view(template_name='login.html',
                                       redirect_authenticated_user=True),   name='login'),
    url(r'^logout/$', Logout.as_view(),                                     name='logout'),
    url(r'^accounts/profile/$', UserRedirect.as_view()),
    url(r'^mostfollowed/$', MostFollowedUsers.as_view()),
    url(r'^admin/', admin.site.urls),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^setlang/(?P<lang>\w+)/$', SetLang.as_view(),                     name='setlang'),
]
