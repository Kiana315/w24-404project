from rest_framework import serializers
from .models import *


class PostSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='author.username')
    class Meta:
        model = Post
        fields = ['id', 'author', 'username', 'title', 'content', 'image', 'visibility', 'date_posted', 'last_modified']
        extra_kwargs = {'author': {'read_only': True}}


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'bio', 'username', 'email', 'avatar']


class CommentSerializer(serializers.ModelSerializer):
    commenter_username = serializers.CharField(source='commenter.username', read_only=True)
    class Meta:
        model = Comment
        fields = ['id', 'post', 'commenter', 'commenter_username', 'date_commented', 'comment_text']


class LikeSerializer(serializers.ModelSerializer):
    liker_username = serializers.CharField(source='liker.username', read_only=True)
    class Meta:
        model = Like
        fields = ['id', 'post', 'liker', 'liker_username', 'date_liked']


class FollowerSerializer(serializers.ModelSerializer):
    follower = UserSerializer(read_only=True)
    following = UserSerializer(read_only=True)
    class Meta:
        model = Follow
        fields = ['id', 'follower', 'following', 'date_followed']

class FriendSerializer(serializers.ModelSerializer):
    user1 = UserSerializer(read_only=True)
    user2 = UserSerializer(read_only=True)
    class Meta:
        model = Friend
        fields = ['id', 'user1', 'user2', 'date_became_friends']
