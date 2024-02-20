from django.contrib import admin
from .models import *


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'date_joined', 'bio')
    search_fields = ('username', 'email')


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'date_posted', 'last_modified')
    search_fields = ('title', 'content')
    list_filter = ('date_posted', 'author')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('commenter', 'date_commented', 'comment_text')
    list_filter = ('date_commented', 'commenter')


class LikeAdmin(admin.ModelAdmin):
    list_display = ('like', 'liker', 'date_liked')
    list_filter = ('date_liked', 'liker')


class FollowerAdmin(admin.ModelAdmin):
    list_display = ('follower', 'following', 'date_followed')
    list_filter = ('date_followed',)
    search_fields = ('follower__username', 'following__username',)


class FriendAdmin(admin.ModelAdmin):
    list_display = ('user1', 'user2', 'date_became_friends')
    list_filter = ('date_became_friends',)
    search_fields = ('user1__username', 'user2__username',)


admin.site.register(User, UserAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Like, LikeAdmin)
admin.site.register(Follower, FollowerAdmin)
admin.site.register(Friend, FriendAdmin)

