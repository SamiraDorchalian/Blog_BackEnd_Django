from rest_framework import serializers
from .models import Author, Post, Comment


class CommentSerializer(serializers.ModelSerializer):
    post_title = serializers.CharField(source='post.title', read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'name', 'email', 'text', 'post', 'post_title']


class PostSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    author_id = serializers.PrimaryKeyRelatedField(source='author', read_only=True)
    comments_count = serializers.IntegerField(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = [
            'id', 'title', 'content', 'cover_photo', 'date_published',
            'slug', 'author', 'author_id', 'comments_count', 'comments'
        ]


class AuthorSerializer(serializers.ModelSerializer):
    posts = serializers.StringRelatedField(many=True, read_only=True)
    posts_count = serializers.SerializerMethodField()

    class Meta:
        model = Author
        fields = [
            'id', 'name', 'avatar', 'field', 'description', 'slug',
            'posts', 'posts_count'
        ]

    def get_posts_count(self, obj):
        return obj.posts.count()