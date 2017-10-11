from django.contrib import admin
from user_profile.models import UserFollower


class UserFollowerAdmin(admin.ModelAdmin):
    list_display = ('user', 'count', 'date')
    ordering = ('-count',)
    search_fields = ('user',)


admin.site.register(UserFollower, UserFollowerAdmin)
