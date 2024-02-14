from django.db import models
from django.contrib.auth.models import AbstractUser

# Inherited from AbstractUser: the User model contains 
# all the fields of Django's built-in user model, 
# such as username, email, password, etc., and you add a custom field.
class User(AbstractUser):
    #A text field used to store the user's personal profile.
    # blank=True indicates that this field is optional 
    # and users can not fill in the introduction when registering
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='static/avatars/', null=True, blank=True)


class Post(models.Model):
    # each Post is associated with a User, if a user is deleted, their posts will also be deleted, allows a user to access all of their posts.
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=255)
    content = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    comment_text = models.TextField()
    date_commented = models.DateTimeField(auto_now_add=True)

class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    date_liked = models.DateTimeField(auto_now_add=True)

class Follower(models.Model):
    follower = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    following = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)
    date_followed = models.DateTimeField(auto_now_add=True)