from django.db import models
from django.contrib.auth.models import AbstractUser

# Choices
FISHING_METHOD = [
    ('Feeder', 'Wędkarstwo morskie'),
    ('Wędkarstwo spławikowe', 'Wędkarstwo muchowe'),
    ('Wędkarstwo gruntowe', 'Spinning'),
]

# Użytkownik
class User(AbstractUser):
    class Meta:
        verbose_name = 'Użytkownik'
        verbose_name_plural = 'Użytkownicy'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True)

    class Meta:
        verbose_name = 'Profil'
        verbose_name_plural = 'Profile'


    def __str__(self):
        return f"{self.user.username}  "



# Miejsce połowu
class FishingSpot(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    description = models.TextField()

    class Meta:
        verbose_name = 'Miejsce Połowu'
        verbose_name_plural = 'Miejsca Połowu'

    def __str__(self):
        return f"{self.name} ({self.location})"


# Gatunek ryby
class FishSpecies(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    season = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Gatunek Ryby'
        verbose_name_plural = 'Gatunki Ryb'

    def __str__(self):
        return f"{self.name}"

# Post na blogu
class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='posts_app')
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='posts_app/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    catches = models.ManyToManyField(
        'Catch',  # Relacja post -> catch, jeden post może mieć wiele połowów
        related_name='post_catches',  # Zmieniamy related_name na 'post_catches'
        blank=True  # Nie jest wymagane posiadanie połowów
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Wpis na blogu'
        verbose_name_plural = 'Wpisy na blogu'

    def __str__(self):
        return f"{self.title} ({self.author})"


# Połów
class Catch(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    species = models.ForeignKey(FishSpecies, on_delete=models.CASCADE, null=False)
    fishing_method = models.CharField(max_length=30, choices=FISHING_METHOD, null=False, default='')
    spot = models.ForeignKey(FishingSpot, on_delete=models.SET_NULL, null=True)
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    date = models.DateField()
    photo = models.ImageField(upload_to='catches/', blank=True)

    class Meta:
        ordering = ['-date']
        verbose_name = 'Połów'
        verbose_name_plural = 'Połowy'

    def __str__(self):
        return f"{self.species.name} {self.weight}kg ({', '.join([post.title for post in self.posts.all()])})"


# Komentarz
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Komentarz'
        verbose_name_plural = 'Komentarze'
    def __str__(self):
        return f"{self.post.title} {self.author} ({self.text}))"
