from django.contrib import admin
from tweets.models import Tweet, HashTag


class TweetAdmin(admin.ModelAdmin):
    list_display = ('user', 'text', 'country', 'created')
    list_filter = ('user', 'country')
    ordering = ('-created',)
    search_fields = ('text',)


class HashTagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


admin.site.register(Tweet, TweetAdmin)
admin.site.register(HashTag, HashTagAdmin)
