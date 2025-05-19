from django.core.management.base import BaseCommand
from faker import Faker
from django.utils.timezone import now
import random

from posts_app.models import (
    User, Profile, FishSpecies, FishingSpot, Catch, Post, Comment, FISHING_METHOD
)

fake = Faker('pl_PL')

class Command(BaseCommand):
    help = "Seed the database with fake fishing-related data"

    def handle(self, *args, **kwargs):
        self.stdout.write("⏳ Seeding data...")
        users = self.create_users(5)
        species = self.create_fish_species()
        spots = self.create_fishing_spots()
        catches = self.create_catches(users, species, spots)
        posts = self.create_posts(users, catches)
        self.create_comments(posts, users)
        self.stdout.write(self.style.SUCCESS("✅ Database seeded successfully."))

    def create_users(self, count):
        users = []
        for _ in range(count):
            user = User.objects.create_user(
                username=fake.user_name(),
                email=fake.email(),
                password='test1234'
            )
            Profile.objects.create(user=user, bio=fake.text(), avatar='')
            users.append(user)
        return users

    def create_fish_species(self):
        fish = []
        for _ in range(5):
            f = FishSpecies.objects.create(
                name=fake.word().capitalize(),
                description=fake.text(),
                season=random.choice(['Wiosna', 'Lato', 'Jesień', 'Zima'])
            )
            fish.append(f)
        return fish

    def create_fishing_spots(self):
        spots = []
        for _ in range(3):
            spot = FishingSpot.objects.create(
                name=fake.city(),
                location=fake.address(),
                description=fake.text()
            )
            spots.append(spot)
        return spots

    def create_catches(self, users, species, spots):
        catches = []
        for _ in range(10):
            catch = Catch.objects.create(
                author=random.choice(users),
                species=random.choice(species),
                fishing_method=random.choice(FISHING_METHOD),
                spot=random.choice(spots),
                weight=round(random.uniform(0.5, 15.0), 2),
                date=fake.date_between(start_date='-1y', end_date='today'),
                photo=''
            )
            catches.append(catch)
        return catches

    def create_posts(self, users, catches):
        posts = []
        for _ in range(5):
            post = Post.objects.create(
                author=random.choice(users),
                title=fake.sentence(nb_words=6),
                content=fake.paragraph(nb_sentences=5),
                image='',
            )
            selected_catches = random.sample(catches, k=random.randint(0, 3))
            post.catches.set(selected_catches)
            posts.append(post)
        return posts

    def create_comments(self, posts, users):
        for _ in range(10):
            Comment.objects.create(
                post=random.choice(posts),
                author=random.choice(users),
                text=fake.sentence(),
            )
