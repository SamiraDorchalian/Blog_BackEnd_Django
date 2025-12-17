from django.shortcuts import render
from rest_framework import viewsets
from django.db.models import Prefetch ,Count
from .models import Author, Post, Comment
from .serializers import AuthorSerializer, PostSerializer, CommentSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_queryset(self):
        return Post.objects.select_related('author').annotate(
            comments_count=Count('comments')
        ).prefetch_related('comments')


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

    def get_queryset(self):
        return Author.objects.annotate(posts_count=Count('posts')).prefetch_related('posts')


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().select_related('post')
    serializer_class = CommentSerializer
