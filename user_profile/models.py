from django.db import models
from django.contrib.auth.models import User


class UserFollower(models.Model):
    user = models.OneToOneField(User)
    date = models.DateTimeField(auto_now_add=True)
    count = models.IntegerField(default=0)
    followers = models.ManyToManyField(User, related_name='followers')

    def __str__(self):
        return self.user.username

    @classmethod
    def create(cls, user):
        user_follower = cls(user=user)
        return user_follower
