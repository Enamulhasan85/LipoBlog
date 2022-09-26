from django.urls import path
from blogs import views
from django.views.generic.base import RedirectView
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('home/', views.home),
    path('', RedirectView.as_view(url='/home')),
    path("blogs/", views.index),
    path("posts/", views.posts)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)