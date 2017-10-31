from django import template


register = template.Library()


@register.simple_tag
def get_selflike(tweet, user):
    return tweet.selflike(user.username)
