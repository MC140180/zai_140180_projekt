from django.contrib import admin

from .models import Post, Profile, Catch, Comment, FishSpecies, FishingSpot
from .models import User

# Register your models here.
admin.site.register(Post)
admin.site.register(User)
admin.site.register(Profile)
admin.site.register(Catch)
admin.site.register(Comment)
admin.site.register(FishSpecies)
admin.site.register(FishingSpot)