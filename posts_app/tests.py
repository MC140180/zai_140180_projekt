import string
import random

from django.test import TestCase

# Create your tests here.
import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from posts_app.models import User, FishSpecies, FishingSpot, Catch, Post, Comment


@pytest.mark.django_db
def test_create_user():
    random_name = ''.join(random.choices(string.ascii_lowercase, k=8))
    User.objects.create_user(username=random_name, email="test@example.com", password="testpass")
    assert User.objects.filter(username=random_name).exists()

@pytest.mark.django_db
def test_create_fish_species():
    random_specie = ''.join(random.choices(string.ascii_lowercase, k=8))
    species = FishSpecies.objects.create(name=random_specie, description="Ryba słodkowodna", season="Lato")
    assert FishSpecies.objects.filter(name=random_specie).exists()

@pytest.mark.django_db
def test_api_get_posts():
    client = APIClient()
    url = reverse("post-list")
    response = client.get(url)
    print(url)
    print(response)
    assert response.status_code == 200

@pytest.mark.django_db
def test_create_fishing_spot():
    random_lake = ''.join(random.choices(string.ascii_lowercase, k=8))
    spot = FishingSpot.objects.create(name=random_lake, location="Mazury", description="Piękne miejsce")
    assert FishingSpot.objects.filter(name="Jezioro").exists()

@pytest.mark.django_db
def test_create_and_get_comment():
    random_comment = ''.join(random.choices(string.ascii_lowercase, k=8))
    user = User.objects.create_user(username=random_comment, password="testpass")
    post = Post.objects.create(author=user, title="Test", content="Test content")
    comment = Comment.objects.create(post=post, author=user, text="Super wpis!")
    assert Comment.objects.filter(text="Super wpis!").exists()


@pytest.mark.django_db
def test_create_post():
    # Przygotowanie danych
    random_user = ''.join(random.choices(string.ascii_lowercase, k=8))
    user = User.objects.create_user(username=random_user, password='testpass')
    post = Post.objects.create(author=user, title='Stary tytuł', content='Stara treść')

    # Przygotowanie klienta
    client = APIClient()
    client.force_authenticate(user=user)

    url = f'/api/posts_app/{post.id}/'  # endpoint do konkretnego posta
    update_data = {
        'title': 'Nowy tytuł',
        'content': 'Nowa treść'
    }
    response = client.put(url, update_data, format='json')

    # Sprawdzenie rezultatu
    assert response.status_code == 200
    assert response.data['title'] == 'Nowy tytuł'
    assert response.data['content'] == 'Nowa treść'


@pytest.mark.django_db
def test_create_new_post():
    # Przygotowanie danych
    random_user = ''.join(random.choices(string.ascii_lowercase, k=8))
    user = User.objects.create_user(username=random_user, password='testpass')

    # Przygotowanie klienta
    client = APIClient()
    client.force_authenticate(user=user)

    # Dane nowego posta
    post_data = {
        'title': 'Nowy post',
        'content': 'Treść nowego posta'
    }

    # Wysłanie żądania
    url = '/api/posts_app/'
    response = client.post(url, post_data, format='json')

    # Sprawdzenie rezultatu
    assert response.status_code == 201
    assert response.data['title'] == 'Nowy post'
    assert response.data['content'] == 'Treść nowego posta'
    assert response.data['author'] == user.id
    assert Post.objects.filter(title='Nowy post').exists()