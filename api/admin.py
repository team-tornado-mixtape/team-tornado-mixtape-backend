from django.contrib import admin
<<<<<<< HEAD
from .models import User, Profile, Mixtape, Song

admin.site.register(User)
admin.site.register(Profile)
=======
from .models import User, Mixtape, Song

admin.site.register(User)
>>>>>>> b9034b67c91053273e0f3a26f25974b7d6993997
admin.site.register(Mixtape)
admin.site.register(Song)
