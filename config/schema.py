import graphene
from graphene_django import DjangoObjectType
from blog.models import Post, Author, Comment

# GraphQL types for models
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

# Query class
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

# Mutation class
class CreateComment(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        email = graphene.String(required=True)
        text = graphene.String(required=True)
        post_slug = graphene.String(required=True)

    ok = graphene.Boolean()
    comment = graphene.Field(CommentType)

    def mutate(self, info, name, email, text, post_slug):
        try:
            post = Post.objects.get(slug=post_slug)
        except Post.DoesNotExist:
            raise Exception("پست پیدا نشد")
        comment = Comment.objects.create(
            name=name,
            email=email,
            text=text,
            post=post,
        )
        return CreateComment(ok=True, comment=comment)

class Mutation(graphene.ObjectType):
    create_comment = CreateComment.Field()

# Schema
schema = graphene.Schema(query=Query, mutation=Mutation)