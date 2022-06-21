from django.contrib import admin
from .models import User, Mixtape, Song

admin.site.register(User)
admin.site.register(Mixtape)
admin.site.register(Song)
