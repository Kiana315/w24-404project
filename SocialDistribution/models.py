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

    def is_friend(self, other_user):
        return self.following.filter(following=other_user).exists() and \
               self.followers.filter(follower=other_user).exists()

    @property
    def avatar_url(self):
        return self.avatar.url if self.avatar else ""

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
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comment', default=99999)
    commenter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='commenters', default=0)
    date_commented = models.DateTimeField(auto_now_add=True)
    comment_text = models.TextField()
    class Meta:
        ordering = ['-date_commented']


class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='like', default=99999)
    liker = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='likers', default=0)
    date_liked = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['-date_liked']


class Follow(models.Model):
    follower = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    following = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)
    date_followed = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ('follower', 'following',)
        ordering = ['-date_followed']

    def are_friends(self, user1, user2):
        return Follow.objects.filter(follower=user1, following=user2).exists() and \
               Follow.objects.filter(follower=user2, following=user1).exists()


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

