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
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth.views import LoginView

from tweets.views import Index, Profile, PostTweet, HashTagPage, Search
from user_profile.views import UserRedirect, MostFollowedUsers, Logout, Signup

urlpatterns = [
    url(r'^$', Index.as_view()),
    url(r'^user/(\w+)/$', Profile.as_view()),
    url(r'^user/(\w+)/post/$', PostTweet.as_view()),
    url(r'^hashtag/(\w+)/$', HashTagPage.as_view()),
    url(r'^search/$', Search.as_view()),
    url(r'^signup/$', Signup.as_view(), name='signup'),
    url(r'^login/$', LoginView.as_view(template_name='login.html'), name='login'),
    url(r'^logout/$', Logout.as_view()),
    url(r'^accounts/profile/$', UserRedirect.as_view()),
    url(r'^mostfollowed/$', MostFollowedUsers.as_view()),
    url(r'^admin/', admin.site.urls),
]
