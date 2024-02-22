# Traditional Pattern:
from django.http import Http404
from django.shortcuts import render, redirect, get_list_or_404
from django.contrib.auth import login, authenticate, get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView, DetailView
from django.db.models import Q
from django.http import JsonResponse


# REST Pattern:
from rest_framework import generics, status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.views import APIView
from rest_framework.response import Response

# Project Dependencies:
from .serializers import *
from .forms import SignUpForm, AvatarUploadForm, UpdateBioForm
from .models import Post
from .permissions import IsAuthorOrReadOnly
from .models import *

User = get_user_model()


"""
---------------------------------- Signup/Login Settings ----------------------------------
"""


class LoginView(LoginView):
    template_name = 'login.html'
    

def signupView(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password1')
        confirm_password = request.POST.get('password2')

        if password == confirm_password:
            # user existence check
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already exists")
                return render(request, 'signup.html')
            elif User.objects.filter(email=email).exists():
                messages.error(request, "Email already exists")
                return render(request, 'signup.html')
            else:
                # create new account
                user = User.objects.create_user(username=username, password=password, email=email)
                user.save()
                user = authenticate(username=username, password=password)
                login(request, user)
                return redirect('login')
        else:
            messages.error(request, "Passwords do not match")
            return render(request, 'signup.html')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


"""
---------------------------------- Posts Presentation Settings ----------------------------------
"""


class PostDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'
    context_object_name = 'post'
    def get_object(self):
        post_id = self.kwargs.get('post_id')
        return get_object_or_404(Post, pk=post_id)


"""
def postView(request, username):
    return render(request, 'post.html')
"""


class IndexView(TemplateView):
    """ * [GET] Get The Home/PP Page """
    template_name = "index.html"


class FriendPostsView(TemplateView):
    """ * [GET] Get The FP Page """
    template_name = "friendPosts.html"


class PPsAPIView(generics.ListAPIView):
    """ [GET] Get The Public Posts """
    serializer_class = PostSerializer
    def get_queryset(self):
        # Get all public posts，sorted by publication time in descending order
        return Post.objects.filter(visibility='PUBLIC').order_by('-date_posted')


class FPsAPIView(generics.ListAPIView):
    """ [GET] Get The Username-based Friend Posts """
    serializer_class = PostSerializer

    def get_queryset(self):
        username = self.kwargs['username']
        user = get_object_or_404(User, username=username)
        return self._getFPsForUser(user)

    def _getFPsForUser(self, user):
        # todo: rule needed
        return user.friend_posts.all()


class NPsAPIView(generics.CreateAPIView):
    """ [POST] Create A New Post """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthorOrReadOnly]
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)  # set current user as author


"""
---------------------------------- Posts Update/Interaction Settings ----------------------------------
"""

#class PostDetailAPIView(generics.CreateAPIView):
#   """ * [GET] Get The Post Detail """
#   template_name = "post_detail.html"


class PostOperationAPIView(generics.RetrieveUpdateDestroyAPIView):
    """ [GET/PUT/DELETE] Get, Update, or Delete A Specific Post """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def get_object(self):
        return get_object_or_404(Post, pk=self.kwargs.get('pk'), author__username=self.kwargs.get('username'))


class CommentAPIView(generics.ListCreateAPIView):
    """ [GET/POST] Get The CommentList For A Spec-post; Create A Comment For A Spec-post """
    serializer_class = CommentSerializer
    def get_queryset(self):
        return get_list_or_404(Comment, post_id=self.kwargs['post_id'])
    def perform_create(self, serializer):
        post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        serializer.save(post=post, user=self.request.user)


class LikeAPIView(generics.ListCreateAPIView):
    """ [GET/POST] Get The LikeList For A Spec-post; Create A Like For A Spec-post """
    serializer_class = LikeSerializer
    def get_queryset(self):
        return get_list_or_404(Like, post_id=self.kwargs['post_id'])
    def perform_create(self, serializer):
        post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        user = self.request.user
        if Like.objects.filter(post=post, user=user).exists():
            raise ValidationError('You have already liked this post.')
        serializer.save(post=post, user=user)


"""
---------------------------------- Message Inbox Settings ----------------------------------
"""


class InboxView(TemplateView):
    """ * [GET] Get The Inbox Page """
    template_name = "inbox.html"


class MsgsAPIView(generics.ListAPIView):
    """ [GET] Get The Inbox Messages """
    queryset = Post.objects.all()
    serializer_class = PostSerializer


"""
----------------------------------  Profile & Identity Settings ----------------------------------
"""


def upload_avatar(request, username):
    if request.method == 'POST':
        form = AvatarUploadForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()

    return redirect(profileView, username=username)


def update_bio(request, username):
    if request.method == 'POST':
        form = UpdateBioForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()

    return redirect(profileView, username=username)


def profileView(request, username):
    user = get_object_or_404(User, username=username)
    context = {
        'user': user,
        'posts': Post.objects.filter(author=user)
    }
    return render(request, 'profile.html', context)



class UserAPIView(generics.RetrieveAPIView):
    """ [GET] Get The Profile Info """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    def get_object(self):
        queryset = self.get_queryset()
        username = self.kwargs.get('username')
        obj = get_object_or_404(queryset, username=username)
        return obj


class FollowerAPIView(generics.ListAPIView):
    """ [GET] Get The FollowerList For A Spec-username """
    serializer_class = FollowerSerializer

    def get_queryset(self):
        username = self.kwargs['username']
        followers = get_list_or_404(Follow, following__username=username)
        return followers
    

class FriendAPIView(generics.ListAPIView):
    """ [GET] Get The FriendList For A Spec-username """
    def get_queryset(self):
        username = self.kwargs['username']
        friends = Friend.objects.filter(Q(user1__username=username) | Q(user2__username=username))
        return friends
    serializer_class = FriendSerializer

def search_user(request):
    query = request.GET.get('q', '')  # Get search query parameters
    try:
        user = User.objects.get(username=query)
        # Or use eamil search：User.objects.get(email=query)
        # Returns a URL pointing to the user's profile
        return JsonResponse({'url': f'/profile/{user.username}/'})
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)
    

class FollowersListView(generics.ListAPIView):
    serializer_class = UserSerializer


    def get_queryset(self):
        username = self.kwargs['username']
        user = User.objects.get(username=username)
        return user.followers.all()  
    
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return render(request, 'followersList.html', {'followers': response.data})

class FollowingListView(generics.ListAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        username = self.kwargs['username']
        user = User.objects.get(username=username)
        return user.following.all()  
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return render(request, 'followingList.html', {'followers': response.data})
    
def follow_user(request, username):
    try:
        user_to_follow = User.objects.get(username=username)
        if user_to_follow != request.user and not Follow.objects.filter(follower=request.user, following=user_to_follow).exists():
            Follow.objects.create(follower=request.user, following=user_to_follow)
            return JsonResponse({"status": "success"}, status=200)
        else:
            return JsonResponse({"error": "Cannot follow"}, status=400)
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found"}, status=404)