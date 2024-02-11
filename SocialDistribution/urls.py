from django.urls import path
from . import views


app_name = "SocialDistribution"
""" May edit this part to have new web pages"""
urlpatterns = [
    # path("", views.index, name="index"),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('following-posts/', views.following_posts_view, name='following_posts'),
    path('public-posts/', views.public_posts_view, name='public_posts'),
    path('profile/<str:username>/', views.profile_view, name='profile'),
    path('inbox/', views.inbox_view, name='inbox'),
    path('post/', views.post_view, name='post'),
    path('server-admin/', views.server_admin_view, name='server_admin'),
    path('friendlist/', views.friendlist_view, name='friendlist'),
]