from django.contrib import admin

from .models import User, Profile, Mixtape, Song

admin.site.register(User)
admin.site.register(Profile)
admin.site.register(Mixtape)
admin.site.register(Song)
