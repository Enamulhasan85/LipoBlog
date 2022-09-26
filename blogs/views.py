from django.shortcuts import render
from .models import post, blogger

# Create your views here.

def home(request):
    return render(request, 'home\index.html')


def index(request):
    return render(request, 'blogs\index.html')


def posts(request):
    posts = post.objects.all()
    return render(request, 'blogs\post.html',{
        'posts': posts
    })