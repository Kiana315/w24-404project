from django.urls import path
from .views import *
from django.contrib import admin
from django.contrib.auth import views as auth_views
from .views import LoginView
from django.contrib.auth.views import LogoutView


app_name = "SocialDistribution"

urlpatterns = [
    path("", IndexView.as_view(), name="home"),
    path('admin/', admin.site.urls, name="admin"),
    path("login/", LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name='logout'),
    path("signup/", signupView, name="signup"),
    path("friendPosts/<str:username>/", FriendPostsView.as_view(), name="friendPosts"),
    path("profile/<str:username>/", profileView, name="profile"),
    path("inbox/<str:username>/", InboxView.as_view(), name="inbox"),
    path("profile/<str:username>/followers", followersListView, name="followers"),
    path("profile/<str:username>/following", followingListView, name="following"),
    path("post/<str:username>", postView, name="post"),
    path("posts/<int:post_id>/", post_detail, name="post_detail"),

    path("api/pps/", PPsAPIView.as_view(), name="API_PPs"),                     # GET PublicPosts
    path("api/fps/<str:username>/", FPsAPIView.as_view(), name="API_FPs"),      # GET FriendPosts
    path("api/nps/", NPsAPIView.as_view(), name="API_NPs"),                     # POST NewPosts
    path("api/msgs/<str:username>/", MsgsAPIView.as_view(), name="API_MSGs"),   # GET InboxMessages
]

