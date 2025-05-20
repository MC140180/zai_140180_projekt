import graphene
from graphene_django.types import DjangoObjectType
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Post, Comment, Catch
from django.contrib.auth import get_user_model
import graphql_jwt

User = get_user_model()

# === Typy ===

class UserType(DjangoObjectType):
    class Meta:
        model = User
        field = "username"

class PostType(DjangoObjectType):
    author = graphene.Field(UserType)

    class Meta:
        model = Post

    def resolve_author(self, info):
        return self.author

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
    posts_by_user = graphene.List(PostType, username=graphene.String())

    def resolve_all_posts(root, info):
        return Post.objects.all()

    def resolve_post(root, info, id):
        try:
            return Post.objects.get(pk=id)
        except Post.DoesNotExist:
            return None

    def resolve_posts_by_user(root, info, username):
        return Post.objects.filter(author__username=username)

# === Mutacje (CREATE, UPDATE, DELETE) ===

class CreatePost(graphene.Mutation):
    class Arguments:
        title = graphene.String()
        content = graphene.String()
        author_id = graphene.Int()

    post = graphene.Field(PostType)

    def mutate(self, info, title, content):
        if not info.context.user.is_authenticated:
            raise Exception("Nie jesteś zalogowany.")
        user = User.objects.get(id=info.context.user.id)
        post = Post(title=title, content=content, author=user)
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
        if not info.context.user.is_authenticated:
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

class JWTMiddleware:
    def resolve(self, next, root, info, **args):
        request = info.context
        auth_header = request.META.get('HTTP_AUTHORIZATION', '').split()
        if auth_header and len(auth_header) == 2 and auth_header[0].lower() == 'bearer':
            jwt_token = auth_header[1]
            try:
                # Wykonaj walidację tokenu
                validated_token = JWTAuthentication().get_validated_token(jwt_token)
                user = JWTAuthentication().get_user(validated_token)
                info.context.user = user
            except:
                info.context.user = None
        return next(root, info, **args)

class Mutation(graphene.ObjectType):
    create_post = CreatePost.Field()
    update_post = UpdatePost.Field()
    delete_post = DeletePost.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)


