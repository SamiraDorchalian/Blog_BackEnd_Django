from django.contrib import admin
from django.utils.html import format_html
from .models import Author, Post, Comment


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['name', 'avatar', 'field',  'slug']
    fields = ['name', 'avatar', 'field', 'description', 'slug']
    search_fields = ['name', 'field']
    list_filter = ['field']
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'content', 'cover_photo', 'date_published', 'slug', 'author']
    fields = ['title', 'content', 'cover_photo', 'date_published', 'slug', 'author']
    list_filter = ['title', 'author']
    search_fields = ['title', 'author__name']
    date_hierarchy = 'date_published'
    prepopulated_fields = {"slug": ("title",)}


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'post']
    list_filter = ['post']
    search_fields = ['name', 'email', 'post__title']
