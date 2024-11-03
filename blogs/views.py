from unicodedata import name
from django.http import HttpResponseNotFound, JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import *
from django.core.files.storage import FileSystemStorage
from django.db.models import Count, F, Max, Subquery, Q
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

    last_500_post_interactions = post_interaction.objects.filter(post__status='published').order_by('-date').values_list('id', flat=True)[:500]
    
    # Group the post_interaction records by post and count the number of 'liked' interactions for each post
    post_interaction_counts = (
        last_500_post_interactions
        .values('post')
        .annotate(liked_count=Count('post', filter=Q(liked=True)))
    )

    # Sort the post objects based on the count of 'liked' interactions in descending order
    sorted_posts = sorted(post_interaction_counts, key=lambda x: x['liked_count'], reverse=True)

    # Retrieve the list of post objects in the sorted order
    posts = post.objects.filter(pk__in=[post['post'] for post in sorted_posts])
    
    print(posts)
    return render(request, 'home\index.html', {'blogger':bloger, 'posts': posts})


def loginpage(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    form = LoginForm(request.POST or None)

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        user = authenticate(request, username=username, password = password)
        if user is not None:
            login(request, user)
            return redirect('blog_home')
        else:
            messages.warning(request, 'Username or Password Incorrect')

    context = {'form': form}
    return render(request, 'accounts/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect("login")


def registerpage(request):
    if request.user.is_authenticated:
        return redirect('home')

    form = CreateUserForm(request.POST or None)
    if request.method == "POST":
        if request.POST.get("password1") != request.POST.get("password2"):
            messages.error(request, "Password and Confirm Password didn't match")
            usergroup = UserGroupForm()
            usergroup.user.first_name = request.POST.get("first_name")
            usergroup.user.last_name = request.POST.get("last_name")
            usergroup.user.username = request.POST.get("username")
            usergroup.user.email = request.POST.get("email")
            
            context = {'user': usergroup}
            return render(request, 'accounts/register.html', context)
            
        if User.objects.filter(username = request.POST.get("username")).exists():
            messages.error(request, "username already exist")
            usergroup = UserGroupForm()
            usergroup.user.first_name = request.POST.get("first_name")
            usergroup.user.last_name = request.POST.get("last_name")
            usergroup.user.username = request.POST.get("username")
            usergroup.user.email = request.POST.get("email")
            
            context = {'user': usergroup}
            return render(request, 'accounts/register.html', context)
            
        user = User()
        user.first_name = request.POST.get("first_name")
        user.last_name = request.POST.get("last_name")
        user.username = request.POST.get("username")
        user.email = request.POST.get("email")
        user.set_password(request.POST.get("password1"))
        user.date_joined = datetime.datetime.now().strftime('%Y-%m-%d')
        user.save()
        messages.success(request, 'Account was created for ' + user.username)
    
        userinfo = blogger(user=authenticate(request, username=user.username, password = user.password))
        userinfo.user = user
        userinfo.fullname = user.first_name + " " + user.last_name
        letters = string.digits
        created = True
        while created:
            result_str = user.username.lower().replace(" ", "-") + ''.join(random.choice(letters) for i in range(9))
            created = blogger.objects.filter(slug=result_str).exists()
        userinfo.slug = result_str
        userinfo.save()
        bloglaout = bloglayout(author=userinfo)
        bloglaout.save()

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


@login_required(login_url='login')
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

    if Post.status == 'draft' and Post.author.user != request.user:
        return HttpResponseNotFound('<h1>Page not found</h1>')

    post_interactionobj = post_interaction()

    if request.user.is_authenticated :
        if post_interaction.objects.filter(post=Post, blogger__user = request.user).exists():
            post_interactionobj = post_interaction.objects.get(post=Post, blogger__user = request.user)

        else:
            post_interactionobj = post_interaction()
            post_interactionobj.post = Post
            post_interactionobj.blogger = blogger.objects.get(user=request.user)
            post_interactionobj.viewed = True
            post_interactionobj.date = datetime.datetime.now()
            post_interactionobj.save()

        if request.method == 'POST':
            post_commentobj = post_comment()
            post_commentobj.post_interaction = post_interactionobj
            post_commentobj.comment = request.POST.get('comment')
            post_commentobj.date = datetime.datetime.now()
            print(post_commentobj.comment)
            post_commentobj.save()

    post_interactionobj.comments = post_comment.objects.filter(post_interaction__post=Post).order_by('-date')[:6]
    return render(request, 'blogs\postview.html', {
            'post': Post,
            'blogger': bloger,
            'post_interaction': post_interactionobj
        })


def likepost(request):
    Post = post.objects.get(id=request.GET.get("postid"))

    if post_interaction.objects.filter(post=Post, blogger__user = request.user).exists():
        post_interactionobj = post_interaction.objects.get(post=Post, blogger__user = request.user)

    else:
        post_interactionobj = post_interaction()
        post_interactionobj.post = Post
        post_interactionobj.blogger = blogger.objects.get(user=request.user)
        post_interactionobj.viewed = True
        post_interactionobj.date = datetime.datetime.now()
        post_interactionobj.save()

    post_interactionobj.liked = post_interactionobj.liked^1
    post_interactionobj.save()

    return JsonResponse({"liked": post_interactionobj.liked}, status=200)


def discoverpost(request):
    bloger = None
    if request.user.is_authenticated:
        bloger = blogger.objects.get(user=request.user)

    categories = Category.objects.all()

    # Filter posts based on the provided criteria
    title = request.GET.get('title', '')
    author = request.GET.get('author', '')
    category_id = request.GET.get('category', '')

    # Start with all posts
    posts = post.objects.filter(status='published')

    # Filter by title
    if title:
        posts = posts.filter(title__icontains=title)

    # Filter by author
    if author:
        posts = posts.filter(author_id=author)

    # Filter by category
    if category_id:
        posts = posts.filter(category_id=category_id)

    # Filter by trending
    if (title or category_id or author) == False:
        last_500_post_interactions = post_interaction.objects.filter(post__status='published').order_by('-date').values_list('id', flat=True)[:1000]
        
        # Group the post_interaction records by post and count the number of 'liked' interactions for each post
        post_interaction_counts = (
            last_500_post_interactions
            .values('post')
            .annotate(liked_count=Count('post', filter=Q(liked=True)))
        )

        # Sort the post objects based on the count of 'liked' interactions in descending order
        sorted_posts = sorted(post_interaction_counts, key=lambda x: x['liked_count'], reverse=True)

        # Retrieve the list of post objects in the sorted order
        posts = post.objects.filter(pk__in=[post['post'] for post in sorted_posts])

    form = PostFilterForm(request.GET or None)
    return render(request, 'blogs\discover.html', {'blogger':bloger, 'categories': categories, 'posts': posts, 'form': form})


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
        userinfo.about = request.POST.get("about")
        userinfo.occupation = request.POST.get("occupation")
        userinfo.save()

        print(request.POST.get("about"))
        user = User.objects.get(id=request.user.id)
        user.email = request.POST.get("email")
        user.save()

    userinfo = blogger.objects.get(user=request.user)
    if userinfo.birthdate != None:
        birthdate = userinfo.birthdate.strftime('%Y-%m-%d')
    else:
        birthdate = datetime.datetime.now().strftime('%Y-%m-%d')

    user = User.objects.get(id=request.user.id)
    userinfo.email = user.email

    return render(request, 'blogs\profile.html', {
            'blogger': userinfo,
            'date':birthdate
        })
