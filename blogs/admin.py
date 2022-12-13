from django.contrib import admin
from .models import *
# Register your models here.

class bloggerAdmin(admin.ModelAdmin):
    list_display = ('user', 'fullname')

class postAdmin(admin.ModelAdmin):
    list_display = ('author', 'date', 'status')

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', )

class bloglayoutAdmin(admin.ModelAdmin):
    list_display = ('author', 'mainfeatured', 'featuredone')

admin.site.register(blogger, bloggerAdmin)
admin.site.register(post, postAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(bloglayout, bloglayoutAdmin)