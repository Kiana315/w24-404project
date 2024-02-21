# forms.py
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')


class AvatarUploadForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['avatar']


class UpdateBioForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['bio']
