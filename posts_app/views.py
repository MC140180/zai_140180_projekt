from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.reverse import reverse
from rest_framework.views import APIView

from .models import Post, Comment, FishSpecies, FishingSpot, Catch, Profile, User
from .permissions import IsAuthorOrReadOnly, IsAdminOrReadOnly, IsProfileAuthorOrReadOnly
from .serializers import (
    PostSerializer, CommentSerializer, FishSpeciesSerializer,
    FishingSpotSerializer, CatchSerializer, ProfileSerializer, UserRegisterSerializer
)
from django.http import JsonResponse


class APIRootView(APIView):
    """
    Widok główny API Root
    """


    def get(self, request, format=None):
        return JsonResponse({
            'posts': reverse('post-list', request=request, format=format),
            'comments': reverse('comment-list', request=request, format=format),
            'species': reverse('species-list', request=request, format=format),
            'spots': reverse('spot-list', request=request, format=format),
            'catches': reverse('catch-list', request=request, format=format),
            'profiles': reverse('profile-list', request=request, format=format),
        })


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = []
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class FishSpeciesViewSet(viewsets.ModelViewSet):
    queryset = FishSpecies.objects.all()
    serializer_class = FishSpeciesSerializer
    permission_classes = [IsAdminOrReadOnly]


class FishingSpotViewSet(viewsets.ModelViewSet):
    queryset = FishingSpot.objects.all()
    serializer_class = FishingSpotSerializer
    permission_classes = [IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CatchViewSet(viewsets.ModelViewSet):
    queryset = Catch.objects.all()
    serializer_class = CatchSerializer
    permission_classes = [IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsProfileAuthorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
