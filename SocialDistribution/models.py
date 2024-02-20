from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    # A text field used to store the user's personal profile.
    #   blank=True indicates that this field is optional
    #   and users can not fill in the introduction when registering
    bio = models.TextField(blank=True)
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField()
    avatar = models.ImageField(upload_to='avatars/', default="default_avatar.jpg")


class Post(models.Model):
    VISIBILITY_CHOICES = [
        ('PUBLIC', 'Public'),
        ('FRIENDS', 'Friends-Only'),
    ]

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=255)
    content = models.TextField()
    image = models.ImageField(upload_to='posts/images/', null=True, blank=True)
    visibility = models.CharField(max_length=10, choices=VISIBILITY_CHOICES, default='PUBLIC')
    date_posted = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    ordering = ['-date_posted']


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    commenter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='commenter', default=1)
    date_commented = models.DateTimeField(auto_now_add=True)
    comment_text = models.TextField()
    ordering = ['-date_commented']


class Like(models.Model):
    like = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    liker = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='liker', default=1)
    date_liked = models.DateTimeField(auto_now_add=True)
    ordering = ['-date_liked']


class Follower(models.Model):
    follower = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    following = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)
    date_followed = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ('follower', 'following',)
        ordering = ['-date_followed']


class Friend(models.Model):
    user1 = models.ForeignKey(User, related_name='friends_set1', on_delete=models.CASCADE)
    user2 = models.ForeignKey(User, related_name='friends_set2', on_delete=models.CASCADE)
    date_became_friends = models.DateTimeField(auto_now_add=True)
    class Meta:
        constraints = [models.UniqueConstraint(fields=['user1', 'user2'], name='unique_friendship')]
        ordering = ['-date_became_friends']
    def clean(self):
        if self.user1 == self.user2:
            raise print("Error: Users cannot be friends with themselves.")

