from django.db import models
from user_profile.models import User


class Tweet(models.Model):
    user = models.ForeignKey(User)
    text = models.CharField(max_length=140)
    created = models.DateTimeField(auto_now_add=True)
    country = models.CharField(max_length=30, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.text


class HashTag(models.Model):
    name = models.CharField(max_length=48, unique=True)
    tweet = models.ManyToManyField(Tweet)

    def __str__(self):
        return self.name
