from unicodedata import name
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from .models import *
from .forms import *
import datetime
import random
import string
import os

# Create your views here.

def home(request):
    bloger = None
    if request.user.is_authenticated:
        bloger = blogger.objects.get(user=request.user)
    
    return render(request, 'home\index.html', {'blogger':bloger})


def loginpage(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        user = authenticate(request, username=username, password = password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.warning(request, 'Username or Password Incorrect')

    context = {}
    return render(request, 'accounts/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect("login")


def registerpage(request):
    if request.user.is_authenticated:
        return redirect('home')

    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for ' + user)
            User = authenticate(request, username=user, password = form.cleaned_data.get('password1'))
            userinfo = blogger(user=User)
            letters = string.digits
            created = True
            while created:
                result_str = user.lower().replace(" ", "-") + ''.join(random.choice(letters) for i in range(9))
                created = blogger.objects.filter(slug=result_str).exists()
            userinfo.slug = result_str
            userinfo.save()
            bloglaout = bloglayout(author=userinfo)
            bloglaout.save()
            return redirect('login')

    context = {'form': form}
    return render(request, 'accounts/register.html', context)


@login_required(login_url='login')
def index(request):
    context = {'blogger': blogger.objects.get(user=request.user)}
    return render(request, 'blogs\index.html', context)


@login_required(login_url='login')
def posts(request):
    blog = blogger.objects.get(user=request.user)
    posts = post.objects.filter(author=blog)
    return render(request, 'blogs\post.html',{
        'posts': posts,
        'blogger': blog
    })


def blog_layout(request):
    bloger = blogger.objects.get(user=request.user)
    layout = bloglayout.objects.get(author=bloger)
    form = LayoutForm()
    if request.method == 'POST':
        layout.mainfeatured = request.POST.get("mainfeatured")
        layout.featuredone = request.POST.get("featuredone")
        layout.featuredtwo = request.POST.get("featuredtwo")
        layout.featuredthree = request.POST.get("featuredthree")
        layout.featuredfour = request.POST.get("featuredfour")
        layout.save()

    posts = post.objects.filter(author=bloger)
    post1 = None
    post2 = None
    post3 = None
    post4 = None
    post5 = None
    if layout.mainfeatured != "": post1 = post.objects.get(slug=layout.mainfeatured)
    if layout.featuredone != "": post2 = post.objects.get(slug=layout.featuredone)
    if layout.featuredtwo != "": post3 = post.objects.get(slug=layout.featuredtwo)
    if layout.featuredthree != "": post4 = post.objects.get(slug=layout.featuredthree)
    if layout.featuredfour != "": post5 = post.objects.get(slug=layout.featuredfour)
    return render(request, 'blogs/bloglayout.html', {
        'blogger': bloger,
        'form': form,
        'post': posts,
        'post1': post1,
        'post2': post2,
        'post3': post3,
        'post4': post4,
        'post5': post5,
    })


def blogview(request, bloggerslug):
    bloger = blogger.objects.get(slug=bloggerslug)
    layout = bloglayout.objects.get(author=bloger)
    category = Category.objects.all()
    post1 = None
    post2 = None
    post3 = None
    post4 = None
    post5 = None
    if layout.mainfeatured != "": post1 = post.objects.get(slug=layout.mainfeatured)
    if layout.featuredone != "": post2 = post.objects.get(slug=layout.featuredone)
    if layout.featuredtwo != "": post3 = post.objects.get(slug=layout.featuredtwo)
    if layout.featuredthree != "": post4 = post.objects.get(slug=layout.featuredthree)
    if layout.featuredfour != "": post5 = post.objects.get(slug=layout.featuredfour)

    Post = None
    if request.method == 'POST':
        Post = post.objects.filter(category=request.POST.get("category"), author=bloger)

    return render(request, 'blogs/blogview.html', {
        'post': Post,
        'blogger': bloger,
        'layout': layout,
        'post1': post1,
        'post2': post2,
        'post3': post3,
        'post4': post4,
        'post5': post5,
        'category': category
    })
        

@login_required(login_url='login')
def createpost(request):
    if request.method == 'GET':
        bloger = blogger.objects.get(user=request.user)
        form = PostForm()
        category = Category.objects.all()
        return render(request, 'blogs\create.html', {'form': form, 'category': category, 'blogger': bloger})
    else:
        postobj = post()
        postobj.title = request.POST.get("title")
        postobj.blogtext = request.POST.get("blogtext")
        postobj.blogimage.delete()
        upload = request.FILES["blogimage"]
        fss = FileSystemStorage()
        file = fss.save('images/' + upload.name, upload)
        postobj.blogimage = 'images/' + upload.name
        postobj.date = datetime.date.today()
        category = None
        if request.POST.get("category") != "":
            category = Category.objects.get(id=request.POST.get("category"))
        elif request.POST.get("category2") != "":
            category = Category(name=request.POST.get("category2"))
            category.save()
        postobj.category = category
        
        letters = string.digits
        created = True
        while created:
            result_str = request.POST.get("title").lower().replace(" ", "-") + "-" + datetime.date.today().strftime("%d-%m-%Y") + ''.join(random.choice(letters) for i in range(9))
            created = post.objects.filter(slug=result_str).exists()
        postobj.slug = result_str
        postobj.location = request.POST.get("location")
        postobj.author = blogger.objects.get(user=request.user)
        postobj.status = request.POST.get("status")
        postobj.save()
        return redirect('posts')


@login_required(login_url='login')
def editpost(request, postslug):
    bloger = blogger.objects.get(user=request.user)
    Post = post.objects.get(slug=postslug)
    if Post.author != bloger:
        return redirect('home')

    if request.method == 'GET':
        form = PostForm(instance=Post)
        form.blogtext = Post.blogtext
        category = Category.objects.all()
        return render(request, 'blogs\edit.html', {
            'post': Post,
            'form': form,
            'category': category,
            'blogger': bloger
        })
    else:
        Post.title = request.POST.get("title")
        Post.blogtext = request.POST.get("blogtext")
        category = None
        if request.POST.get("category") != "":
            category = Category.objects.get(id=request.POST.get("category"))
        elif request.POST.get("category2") != "":
            category = Category(name=request.POST.get("category2"))
            category.save()
        Post.category = category

        if request.FILES.get("blogimage", False):
            Post.blogimage.delete()
            upload = request.FILES["blogimage"]
            fss = FileSystemStorage()
            file = fss.save('images/' + upload.name, upload)
            Post.blogimage = 'images/' + upload.name
        Post.date = datetime.date.today()
        Post.location = request.POST.get("location")
        Post.author = blogger.objects.get(user=request.user)
        Post.status = request.POST.get("status")
        Post.save()
        return redirect('posts')


@login_required(login_url='login')
def deletepost(request, postslug):
    if request.method == 'POST':
        post.objects.filter(slug=postslug).delete()
        return redirect('posts')
 

def postview(request, postslug):
    Post = post.objects.get(slug=postslug)
    bloger = Post.author
    return render(request, 'blogs\postview.html', {
            'post': Post,
            'blogger': bloger
        })


@login_required(login_url='login')
def profile(request):
    userinfo = blogger.objects.get(user=request.user)
    if request.method == 'POST':
        userinfo.fullname = request.POST.get("fullname")
        userinfo.birthdate = request.POST.get("birthdate")
        userinfo.gender = request.POST.get("gender")
        if request.FILES.get("image", False):
            userinfo.image.delete()
            upload = request.FILES["image"]
            fss = FileSystemStorage()
            file = fss.save('images/' + upload.name, upload)
            userinfo.image = 'images/' + upload.name
        userinfo.address = request.POST.get("Address")
        userinfo.education = request.POST.get("education")
        userinfo.occupation = request.POST.get("occupation")
        userinfo.save()

    userinfo = blogger.objects.get(user=request.user)
    if userinfo.birthdate != None:
        birthdate = userinfo.birthdate.strftime('%Y-%m-%d')
    else:
        birthdate = datetime.datetime.now().strftime('%Y-%m-%d')
    return render(request, 'blogs\profile.html', {
            'blogger': userinfo,
            'date':birthdate
        })
