from django import forms
from blogs import models
from ckeditor.widgets import CKEditorWidget
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

        
class PostForm(forms.ModelForm):
    class Meta:
       model = models.post
       fields = ['blogtext']


class LayoutForm(forms.ModelForm):
    class Meta:
       model = models.bloglayout
       fields = ['author', 'mainfeatured', 'featuredone', 'featuredtwo', 'featuredthree', 'featuredfour']


       




