from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class blogger(models.Model):
    firstname = models.CharField(max_length=200)
    lastname = models.CharField(max_length=200)
    address = models.CharField(max_length=250)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.firstname} {self.lastname}'

class post(models.Model):
    status = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )

    title = models.CharField(max_length=200)
    blogtext = models.TextField()
    blogimage = models.ImageField(upload_to='images')
    date = models.DateField()
    slug = models.SlugField(max_length=200)
    location = models.CharField(max_length=200)
    author = models.ForeignKey(blogger, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=status, default='draft')

    def __str__(self):
        return f'{self.title} ({self.date})'
