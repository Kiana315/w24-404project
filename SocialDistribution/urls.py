from django.urls import path
from . import views


app_name = "SocialDistribution"
""" May edit this part to have new web pages"""
urlpatterns = [
    path("", views.index, name="index"),
  
]