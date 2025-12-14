import graphene
from graphene_django import DjangoObjectType
from blog.models import Post, Author, Comment


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


class Query(graphene.ObjectType):
    all_posts = graphene.List(PostType)
    all_authors = graphene.List(AuthorType)
    
    # اضافه کردن کوئری جدید برای کامنت‌های یک پست
    comments_by_post_slug = graphene.List(CommentType, slug=graphene.String(required=True))
    
    post_by_slug = graphene.Field(PostType, slug=graphene.String(required=True))
    posts_by_author = graphene.List(PostType, author_name=graphene.String())

    def resolve_all_posts(root, info):
        return Post.objects.all()

    def resolve_all_authors(root, info):
        return Author.objects.all()

    # جدید: کامنت‌های یک پست خاص
    def resolve_comments_by_post_slug(root, info, slug):
        try:
            post = Post.objects.get(slug=slug)
            return Comment.objects.filter(post=post)
        except Post.DoesNotExist:
            return []

    def resolve_post_by_slug(root, info, slug):
        try:
            return Post.objects.get(slug=slug)
        except Post.DoesNotExist:
            return None

    def resolve_posts_by_author(root, info, author_name):
        return Post.objects.filter(author__name__icontains=author_name)


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
            raise graphene.GraphQLError("پست مورد نظر پیدا نشد")

        comment = Comment.objects.create(
            name=name,
            email=email,
            text=text,
            post=post,
        )
        return CreateComment(ok=True, comment=comment)


class Mutation(graphene.ObjectType):
    create_comment = CreateComment.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)