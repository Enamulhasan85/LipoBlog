from django.urls import path
from blogs import views
from django.views.generic.base import RedirectView
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', RedirectView.as_view(url='/home')),
    path('home/', views.home, name='home'),
    path('register/', views.registerpage, name='register'),
    path('login/', views.loginpage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('profile/', views.profile, name='profile'),
    path("blogs/", views.index, name='blog_home'),
    path("posts/", views.posts, name='posts'),
    path("bloglayout/", views.blog_layout, name='blog_layout'),
    path("blogview/<slug:bloggerslug>", views.blogview, name='blog_view'),
    path("posts/create/", views.createpost, name='post_create'),
    path("posts/edit/<slug:postslug>", views.editpost, name='post_edit'),
    path("posts/view/<slug:postslug>", views.postview, name='post_view'),
    path("posts/delete/<slug:postslug>", views.deletepost, name='post_delete'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)