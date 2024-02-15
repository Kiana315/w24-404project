from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from .forms import SignUpForm
from django.contrib import messages

User = get_user_model()
# def loginView(request):
#     return render(request, 'login.html')
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
    


def indexView(request):
    return render(request, 'index.html')


def profileView(request, username):
    # user = get_object_or_404(User, username=username)
    # context = {'profile_user': user}
    # return render(request, 'profile.html', context)
    return render(request, 'profile.html')

def signup_view(request):
    return render(request, 'signup.html')   

def inboxView(request):
    return render(request, 'inBox.html')


def friendPostsView(request, username):
    # user = get_object_or_404(User, username=username)
    # context = {'profile_user': user}
    # return render(request, 'profile.html', context)
    return render(request, 'friendPosts.html')

def followersListView(request, username):
    return render(request, 'peopleList.html')

def followingListView(request, username):
    return render(request, 'peopleList.html')

