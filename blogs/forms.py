from django import forms
from blogs.models import *
from ckeditor.widgets import CKEditorWidget
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

     
class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", 'password']
        widgets = {
            "username": forms.TextInput(attrs={}),
            "password": forms.TextInput(attrs={'type': 'password'}),
        }
   
        
class UserGroupForm(UserCreationForm):
        id = forms.IntegerField()
        username = forms.CharField(max_length=150)
        first_name = forms.CharField(max_length=150)
        last_name = forms.CharField(max_length=150)
        email = forms.EmailField()
        is_active = models.BooleanField(default=True)
        user = User()
        

class PostForm(forms.ModelForm):
    class Meta:
       model = post
       fields = ['blogtext']



class PostFilterForm(forms.ModelForm):
    class Meta:
       model = post
       fields = ['author', 'title', 'category']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set required attribute to False for each field you want to make optional
        self.fields['author'].required = False
        self.fields['title'].required = False
        self.fields['category'].required = False

class LayoutForm(forms.ModelForm):
    class Meta:
       model = bloglayout
       fields = ['author', 'mainfeatured', 'featuredone', 'featuredtwo', 'featuredthree', 'featuredfour']


       




