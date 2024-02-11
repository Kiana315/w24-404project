from django.urls import path
from . import views
from django.contrib import admin
from django.contrib.auth import views as auth_views


app_name = "SocialDistribution"

urlpatterns = [
    path("", views.indexView, name="home"),
    path('admin/', admin.site.urls, name="admin"),
    path("home/", views.indexView, name="home"),
    path("login/", views.loginView, name="login"),
    path("signup/", views.signupView, name="signup"),
    path("friendPosts/<str:username>/", views.signupView, name="friendPosts"),
    path("profile/<str:username>/", views.profileView, name="profile"),
    path("inBox/", views.inboxView, name="inbox"),
]

