from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.db.models import Prefetch
from .models import Author, Post, Comment


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['name', 'avatar_thumbnail', 'field', 'slug']
    list_display_links = ['name']
    fields = ['name', 'avatar', 'avatar_preview', 'field', 'description', 'slug']
    readonly_fields = ['avatar_preview']
    search_fields = ['name', 'field']
    list_filter = ['field']
    prepopulated_fields = {"slug": ("name",)}


    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.prefetch_related('posts')


    def avatar_thumbnail(self, obj):
        if obj.avatar:
            return format_html(
                '<img src="{}" width="50" height="50" style="object-fit: cover; border-radius: 4px;" />',
                obj.avatar.url
            )
        return "-"
    avatar_thumbnail.short_description = "آواتار"


    def avatar_preview(self, obj):
        if obj.avatar:
            return format_html(
                '<img src="{}" width="300" style="border-radius: 8px;" />',
                obj.avatar.url
            )
        return "(تصویری انتخاب نشده)"
    avatar_preview.short_description = "پیش‌نمایش آواتار"


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'cover_photo_thumbnail', 'author', 'date_published', 'slug']
    list_display_links = ['title']
    fields = ['title', 'content', 'cover_photo', 'cover_photo_preview', 'date_published', 'slug', 'author']
    readonly_fields = ['cover_photo_preview']
    list_filter = ['author', 'date_published']
    search_fields = ['title', 'author__name', 'content']
    date_hierarchy = 'date_published'
    prepopulated_fields = {"slug": ("title",)}
    

    list_select_related = ('author',) 


    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('author').prefetch_related('comments')


    def cover_photo_thumbnail(self, obj):
        if obj.cover_photo:
            return format_html(
                '<img src="{}" width="80" height="50" style="object-fit: cover; border-radius: 4px;" />',
                obj.cover_photo.url
            )
        return "-"
    cover_photo_thumbnail.short_description = "کاور"

    def cover_photo_preview(self, obj):
        if obj.cover_photo:
            return format_html(
                '<img src="{}" width="500" style="max-width: 100%; height: auto; border-radius: 8px;" />',
                obj.cover_photo.url
            )
        return "(تصویری انتخاب نشده)"
    cover_photo_preview.short_description = "پیش‌نمایش کاور"


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'post_title', 'post']
    list_filter = ['post__title', 'post__author']
    search_fields = ['name', 'email', 'text', 'post__title', 'post__author__name']
    

    list_select_related = ('post', 'post__author')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('post', 'post__author')


    def post_title(self, obj):
        return obj.post.title if obj.post else "-"
    post_title.short_description = "عنوان پست"
    post_title.admin_order_field = 'post__title'
    