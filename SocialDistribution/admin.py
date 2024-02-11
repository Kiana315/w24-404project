from django.contrib import admin
from .models import User, Post, Comment, Like, Follower

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'date_joined', 'bio')
    search_fields = ('username', 'email')

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'date_posted', 'last_modified')
    search_fields = ('title', 'content')
    list_filter = ('date_posted', 'author')

class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'date_commented', 'comment_text')
    search_fields = ('comment_text',)
    list_filter = ('date_commented', 'author')

class LikeAdmin(admin.ModelAdmin):
    list_display = ('post', 'user', 'date_liked')

class FollowerAdmin(admin.ModelAdmin):
    list_display = ('follower', 'following', 'date_followed')

admin.site.register(User, UserAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Like, LikeAdmin)
admin.site.register(Follower, FollowerAdmin)
