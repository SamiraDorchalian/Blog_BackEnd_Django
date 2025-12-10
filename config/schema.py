import graphene
from graphene_django import DjangoObjectType
from blog.models import Post, Author, Comment

# GraphQL for models
class AuthorType(DjangoObjectType):
    class Meta:
        model = Author
        fields = "__all__"

class PostType(DjangoObjectType):
    class Meta:
        model = Post
        fields = "__all__"

class CommentType(DjangoObjectType):
    class Meta:
        model = Comment
        fields = "__all__"

#Query
class Query(graphene.ObjectType):
    all_posts = graphene.List(PostType)
    all_authors = graphene.List(AuthorType)
    all_comments = graphene.List(CommentType)

    post_by_slug = graphene.Field(PostType, slug=graphene.String())
    posts_by_author = graphene.List(PostType, author_name=graphene.String())

    def resolve_all_posts(root, info):
        return Post.objects.all()

    def resolve_all_authors(root, info):
        return Author.objects.all()

    def resolve_all_comments(root, info):
        return Comment.objects.all()

    def resolve_post_by_slug(root, info, slug):
        try:
            return Post.objects.get(slug=slug)
        except Post.DoesNotExist:
            return None

    def resolve_posts_by_author(root, info, author_name):
        return Post.objects.filter(author__name__icontains=author_name)


schema = graphene.Schema(query=Query)
