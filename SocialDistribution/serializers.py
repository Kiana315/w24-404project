from rest_framework import serializers
from .models import Post


class PostSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='author.username')
    class Meta:
        model = Post
        fields = ['id', 'author', 'username', 'title', 'content', 'image', 'visibility', 'date_posted', 'last_modified']
        extra_kwargs = {'author': {'read_only': True}}