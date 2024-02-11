from django.shortcuts import render
from django.contrib.auth.models import User


def loginView(request):
    return render(request, 'login.html')


def signupView(request):
    return render(request, 'signup.html')


def indexView(request):
    return render(request, 'index.html')


def profileView(request, username):
    # user = get_object_or_404(User, username=username)
    # context = {'profile_user': user}
    # return render(request, 'profile.html', context)
    return render(request, 'profile.html')


def inboxView(request):
    return render(request, 'inBox.html')


def friendPostsView(request, username):
    # user = get_object_or_404(User, username=username)
    # context = {'profile_user': user}
    # return render(request, 'profile.html', context)
    return render(request, 'friendPosts.html')