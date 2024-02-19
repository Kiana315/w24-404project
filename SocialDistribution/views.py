# Traditional Pattern:
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

# REST Pattern:
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response

# Project Dependencies:
from .serializers import PostSerializer
from .forms import SignUpForm
from .models import Post
from .permissions import IsAuthorOrReadOnly

"""
+++++++++++++++++++++++++++++++++++ Basic Views +++++++++++++++++++++++++++++++++++
"""
User = get_user_model()


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


def profileView(request, username):
    user = get_object_or_404(User, username=username)
    context = {'profile_user': user}
    return render(request, 'profile.html', context)


def signup_view(request):
    return render(request, 'signup.html')   


def inboxView(request, username):
    return render(request, 'inbox.html')


def followersListView(request, username):
    return render(request, 'peopleList.html')


def followingListView(request, username):
    return render(request, 'peopleList.html')


def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    return render(request, 'post_detail.html', {'post': post})


def postView(request, username):
    
    return render(request, 'post.html')


"""
+++++++++++++++++++++++++++++++++++ REST-based Views +++++++++++++++++++++++++++++++++++
"""


class IndexAPIView(TemplateView):
    """ * [GET] Get The Home/PP Page """
    template_name = "index.html"


class FriendPostsAPIView(TemplateView):
    """ * [GET] Get The FP Page """
    template_name = "friendPosts.html"


class PPsAPIView(generics.ListAPIView):
    """ [GET] Get The Public Posts """
    queryset = Post.objects.filter(visibility='PUBLIC')
    serializer_class = PostSerializer


class FPsAPIView(generics.ListAPIView):
    """ [GET] Get The Username-based Friend Posts """
    serializer_class = PostSerializer

    def get_queryset(self):
        username = self.kwargs['username']
        user = get_object_or_404(User, username=username)
        return self._getFPsForUser(user)

    def _getFPsForUser(self, user):
        return user.friend_posts.all()


class NPsAPIView(generics.CreateAPIView):
    """ [POST] Create A New Post """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthorOrReadOnly]  

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)  # set current user as author


class PostDetailView(generics.CreateAPIView):
    """ [GET] Get The Post Detail """
    template_name = "post_detail.html"