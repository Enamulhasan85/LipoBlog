from django.contrib import admin
from .models import blogger, post
# Register your models here.

class bloggerAdmin(admin.ModelAdmin):
    list_display = ('firstname', 'user')

class postAdmin(admin.ModelAdmin):
    list_display = ('author', 'date', 'status')

admin.site.register(blogger, bloggerAdmin)
admin.site.register(post, postAdmin)