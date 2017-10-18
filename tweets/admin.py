from django.contrib import admin
from tweets.models import Tweet, HashTag, Like, Retweet, Comment


class TweetAdmin(admin.ModelAdmin):
    list_display = ('user', 'text', 'country', 'created')
    list_filter = ('user', 'country')
    ordering = ('-created',)
    search_fields = ('text',)


class HashTagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


class LikeAdmin(admin.ModelAdmin):
    list_display = ('tweet',)
    search_fields = ('tweet',)


class RetweetAdmin(admin.ModelAdmin):
    list_display = ('tweet', 'user', 'is_active',)
    list_filter = ('user', 'is_active',)
    search_fields = ('tweet', 'user',)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('tweet', 'user', 'text', 'is_active', 'created')
    list_filter = ('user', 'is_active',)
    ordering = ('-created',)
    search_fields = ('text', 'user', 'tweet')


admin.site.register(Tweet, TweetAdmin)
admin.site.register(HashTag, HashTagAdmin)
admin.site.register(Like, LikeAdmin)
admin.site.register(Retweet, RetweetAdmin)
admin.site.register(Comment, CommentAdmin)
