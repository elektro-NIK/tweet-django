from django.db import models
from user_profile.models import User


class Tweet(models.Model):
    user = models.ForeignKey(User)
    text = models.CharField(max_length=140)
    created = models.DateTimeField(auto_now_add=True)
    country = models.CharField(max_length=30, blank=True)
    is_active = models.BooleanField(default=True)

    def selflike(self):
        return self.user in self.like.users.all()

    def retweets(self):
        return Retweet.objects.filter(tweet=self).order_by('-created')

    def count_retweets(self):
        return self.retweets().count() or ''

    def comments(self):
        return Comment.objects.filter(tweet=self)

    def count_comments(self):
        return self.comments().count() or ''

    def __str__(self):
        return self.text


class HashTag(models.Model):
    name = models.CharField(max_length=25, unique=True)
    tweet = models.ManyToManyField(Tweet)

    def __str__(self):
        return self.name


class Like(models.Model):
    tweet = models.OneToOneField(Tweet)
    users = models.ManyToManyField(User)

    def __str__(self):
        return self.tweet.text


class Retweet(models.Model):
    tweet = models.ForeignKey(Tweet)
    user = models.ForeignKey(User)
    created = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.tweet.text


class Comment(models.Model):
    tweet = models.ForeignKey(Tweet)
    user = models.ForeignKey(User)
    text = models.CharField(max_length=280)
    created = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.text
