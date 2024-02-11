from django.shortcuts import render, redirect
from django.http import HttpResponse

from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

# Todo: Fell free to edit, just copy from lab3
from .models import User, Post, Comment, Like, Follower

from rest_framework.decorators import api_view
from rest_framework.response import Response




def login_view(request):
    return render(request, 'login.html')

def signup_view(request):
    return render(request, 'signup.html')   

def following_posts_view(request):
    return render(request, 'followign_posts.html')

def public_posts_view(request):
    return render(request, 'public_posts.html')

def profile_view(request, username):
    return render(request, 'profile.html', {'username': username})

def inbox_view(request):
    return render(request, 'inbox.html')

def post_view(request):
    return render(request, 'post.html')

def server_admin_view(request):
    return render(request, 'server_admin.html')

def friendlist_view(request):
    return render(request, 'friendlist.html')


# # Todo: Fell free to edit all the following codes, just copy from lab3
# class IndexView(generic.TemplateView):
#     """ Define the PublicPost Page (Main Page))"""
#     template_name = "SocialDistribution/index.html"
#     context_object_name = "latest_question_list"

#     def get_queryset(self):
#         """Return the last five published questions."""
#         return Question.objects.order_by("-pub_date")[:5]


# class DetailView(generic.DetailView):
#     model = Question
#     template_name = "polls/detail.html"


# class ResultsView(generic.DetailView):
#     model = Question
#     template_name = "polls/results.html"


# def vote(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     try:
#         selected_choice = question.choice_set.get(pk=request.POST["choice"])
#     except (KeyError, Choice.DoesNotExist):
#         # Redisplay the question voting form.
#         return render(
#             request,
#             "polls/detail.html",
#             {
#                 "question": question,
#                 "error_message": "You didn't select a choice.",
#             },
#         )
#     else:
#         selected_choice.votes += 1
#         selected_choice.save()
#         # Always return an HttpResponseRedirect after successfully dealing
#         # with POST data. This prevents data from being posted twice if a
#         # user hits the Back button.
#         return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))


# @api_view(['GET'])
# def get_questions(request):
#     """
#     Get the list of questions on our website
#     """
#     questions = Question.objects.all()
#     serializer = QuestionSerializer(questions, many=True)
#     return Response(serializer.data)


# @api_view(['GET', 'POST'])
# def update_question(request, pk):
#     """
#     Get the list of questions on our website
#     """
#     questions = Question.objects.get(id=pk)
#     serializer = QuestionSerializer(questions, data=request.data, partial=True)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data)
#     return Response(status=400, data=serializer.errors)
