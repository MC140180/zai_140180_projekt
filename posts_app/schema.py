import graphene
from graphene_django.types import DjangoObjectType
from .models import Post, Comment, Catch
from django.contrib.auth import get_user_model
import graphql_jwt

User = get_user_model()

# === Typy ===

class PostType(DjangoObjectType):
    class Meta:
        model = Post

class CommentType(DjangoObjectType):
    class Meta:
        model = Comment

class CatchType(DjangoObjectType):
    class Meta:
        model = Catch

# === Zapytania (QUERY) ===

class Query(graphene.ObjectType):
    all_posts = graphene.List(PostType)
    post = graphene.Field(PostType, id=graphene.Int())

    def resolve_all_posts(root, info):
        return Post.objects.all()

    def resolve_post(root, info, id):
        try:
            return Post.objects.get(pk=id)
        except Post.DoesNotExist:
            return None

# === Mutacje (CREATE, UPDATE, DELETE) ===

class CreatePost(graphene.Mutation):
    class Arguments:
        title = graphene.String()
        content = graphene.String()
        category = graphene.String()
        author_id = graphene.Int()

    post = graphene.Field(PostType)

    def mutate(self, info, title, content, category, author_id):
        if info.context.user.is_anonymous:
            raise Exception("Nie jesteś zalogowany.")
        user = User.objects.get(id=author_id)
        post = Post(title=title, content=content, category=category, author=user)
        post.save()
        return CreatePost(post=post)

class UpdatePost(graphene.Mutation):
    class Arguments:
        id = graphene.Int()
        title = graphene.String()
        content = graphene.String()
        category = graphene.String()

    post = graphene.Field(PostType)

    def mutate(self, info, id, title=None, content=None, category=None):
        post = Post.objects.get(pk=id)
        if info.context.user.is_anonymous:
            raise Exception("Nie jesteś zalogowany.")
        if post.author != info.context.user:
            raise Exception("Nie masz uprawnień do edytowania tego posta.")
        if title:
            post.title = title
        if content:
            post.content = content
        if category:
            post.category = category
        post.save()
        return UpdatePost(post=post)

class DeletePost(graphene.Mutation):
    class Arguments:
        id = graphene.Int()

    ok = graphene.Boolean()

    def mutate(self, info, id):
        post = Post.objects.get(pk=id)
        if info.context.user.is_anonymous:
            raise Exception("Nie jesteś zalogowany.")
        if post.author != info.context.user:
            raise Exception("Nie masz uprawnień do edytowania tego posta.")
        try:
            post = Post.objects.get(pk=id)
            post.delete()
            return DeletePost(ok=True)
        except Post.DoesNotExist:
            return DeletePost(ok=False)

# === Rejestracja mutacji ===

class Mutation(graphene.ObjectType):
    create_post = CreatePost.Field()
    update_post = UpdatePost.Field()
    delete_post = DeletePost.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
