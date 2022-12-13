from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from ckeditor.fields import RichTextField
# Create your models here.

GENDER = (
    ('M', 'Male'),
    ('F', 'Female'),
)

class blogger(models.Model):
    fullname = models.CharField(max_length=400, blank=True)
    birthdate = models.DateField(null=True, blank=True)
    gender = models.CharField(choices=GENDER, max_length=20, default='M', blank=True, null=True)
    address = models.CharField(max_length=250, blank=True)
    occupation = models.CharField(max_length=250, blank=True)
    education = models.CharField(max_length=250, blank=True)
    image = models.ImageField(upload_to='images')
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f'{self.user}'


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class post(models.Model):
    status = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )

    title = models.CharField(max_length=200)
    blogtext = RichTextField(blank=True, null=True)
    blogimage = models.ImageField(upload_to='images')
    date = models.DateField()
    slug = models.SlugField(max_length=200)
    location = models.CharField(max_length=200)
    author = models.ForeignKey(blogger, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=status, default='draft')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f'{self.title} ({self.date})'


class bloglayout(models.Model):
    author = models.ForeignKey(blogger, on_delete=models.CASCADE)
    mainfeatured = models.SlugField(max_length=200, blank=True)
    featuredone = models.SlugField(max_length=200, blank=True)
    featuredtwo = models.SlugField(max_length=200, blank=True)
    featuredthree = models.SlugField(max_length=200, blank=True)
    featuredfour = models.SlugField(max_length=200, blank=True)

