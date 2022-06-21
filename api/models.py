from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

    def __repr__(self):
        return f"<User username={self.username} pk={self.pk}>"

    def __str__(self):
        return self.username


class Profile(models.Model):
<<<<<<< HEAD
    user        = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at  = models.DateTimeField(auto_now_add=True)
    followers   = models.ManyToManyField(User, related_name='followers')
    image       = models.ImageField(upload_to='files/profilepics')
=======
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    spotify_username = models.CharField(default='', max_length=255)
    spotify_password = models.CharField(default='', max_length=255)
    spotify_created_at = models.DateTimeField()
    apple_music_username = models.CharField(default='', max_length=255)
    apple_music_password = models.CharField(default='', max_length=255)
    apple_music_created_at = models.DateTimeField()
    friends = models.ManyToManyField(User, related_name='friends', blank=True)
    followers = models.ManyToManyField(User, related_name='followers', blank=True)

    def friend_count(self):
        return self.friends.count()
>>>>>>> b9034b67c91053273e0f3a26f25974b7d6993997

    def follower_count(self):
        return self.followers.count()

# The following lines of code can be added to add functionality to the connection model.
    # def get_connections(self):
    #     connections = Connection.objects.filter(creator=self.user)
    #     return connections

    # def get_followers(self):
    #     followers   = Connection.objects.filter(following=self.user)
    #     return followers



class Mixtape(models.Model):
<<<<<<< HEAD
    created_at   = models.DateTimeField(auto_now_add=True)
    creator      = models.ForeignKey(User, related_name='creator', on_delete=models.CASCADE)
    title        = models.CharField(max_length=255)
    is_public    = models.BooleanField(default=False)
    description  = models.TextField()
    modified_at  = models.DateTimeField(auto_now=True)
=======
    created_at = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(User, related_name='creator', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    is_public = models.BooleanField(default=True)
    description = models.TextField()
    modified_at = models.DateTimeField(auto_now=True)
>>>>>>> b9034b67c91053273e0f3a26f25974b7d6993997
    favorited_by = models.ManyToManyField(User, related_name='favorite_mixtapes', blank=True)

    def favorite_count(self):
        return self.favorited_by.count()

    def __repr__(self):
        return f"<User username={self.title} pk={self.pk}>"

    def __str__(self):
        return self.title


class Song(models.Model):
    created_at          = models.DateTimeField(auto_now_add=True)
    spotify_title       = models.TextField()
    spotify_artist      = models.TextField()
    spotify_album       = models.TextField()
    spotify_url         = models.TextField()
    apple_music_title   = models.TextField()
    apple_music_artist  = models.TextField()
    apple_music_album   = models.TextField()
    apple_music_url     = models.TextField()
    spotify_preview_url = models.TextField()
    mixtapes            = models.ManyToManyField(Mixtape, related_name='mixtapes', blank=True)
    favorited_by        = models.ManyToManyField(User, related_name='favorite_songs')

    def favorite_count(self):
        return self.favorited_by.count()

    def __repr__(self):
        return f"<User username={self.spotify_title} pk={self.pk}>"

    def __str__(self):
        return self.spotify_title

# the following model can be added to create connections between users
# class Connection(models.Model):
#     created   = models.DateTimeField(auto_now_add=True, editable=False)
#     creator   = models.ForeignKey(User, related_name="friendship_creator_set")
#     following = models.ForeignKey(User, related_name="friend_set")


