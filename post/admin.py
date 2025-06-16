from django.contrib import admin
from .models import Post, SavedPost, Category

admin.site.register(Post)
admin.site.register(SavedPost)
admin.site.register(Category)