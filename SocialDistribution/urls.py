from django.urls import path
from . import views
from django.contrib import admin
from django.contrib.auth import views as auth_views
from .views import LoginView
from django.contrib.auth.views import LogoutView

app_name = "SocialDistribution"

urlpatterns = [
    path("", views.indexView, name="home"),
    path('admin/', admin.site.urls, name="admin"),
    path("login/", LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name='logout'),
    path("signup/", views.signupView, name="signup"),
    path("friendPosts/<str:username>/", views.friendPostsView, name="friendPosts"),
    path("profile/<str:username>/", views.profileView, name="profile"),
    path("inbox/<str:username>/", views.inboxView, name="inbox"),
    path("profile/<str:username>/followers", views.followersListView, name="followers"),
    path("profile/<str:username>/following", views.followingListView, name="following"),
    path("post/<str:username>", views.postView, name="post"),
]

