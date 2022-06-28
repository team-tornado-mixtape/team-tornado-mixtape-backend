from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    def __repr__(self):
        return f"<User username={self.username} pk={self.pk}>"

    def __str__(self):
        return self.username


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profiles')
    created_at = models.DateTimeField(auto_now_add=True)
    followed_by = models.ManyToManyField(User, related_name="followers")

    def follower_count(self):
        return self.followed_by.count()
    
    def get_user_id(self):
        return self.user.pk
    
    def get_username(self):
        return self.user.username

    def get_first_name(self):
        return self.user.first_name
    
    def get_last_name(self):
        return self.user.last_name

    def __str__(self):
        return self.user.username



class Image(models.Model):
    uploaded_at = models.DateTimeField(auto_now_add=True)
    picture = models.ImageField(blank=True, null=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='images')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='images')
    
    def __img__(self):
        return self.picture

    


# The following lines of code can be added to add functionality to the connection model.
# def get_connections(self):
#     connections = Connection.objects.filter(creator=self.user)
#     return connections

# def get_followers(self):
#     followers   = Connection.objects.filter(following=self.user)
#     return followers


class Mixtape(models.Model):

    created_at = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(User, related_name="mixtapes", on_delete=models.CASCADE,null=True)
    title = models.CharField(max_length=255, default="")
    is_public = models.BooleanField(default=False)
    description = models.TextField(default="")
    modified_at = models.DateTimeField(auto_now=True)
    theme = models.IntegerField(default="0")
    favorited_by = models.ManyToManyField(
        User, related_name="favorite_mixtapes", blank=True
    )

    def favorite_count(self):
        return self.favorited_by.count()

    def __repr__(self):
        return f"<User username={self.title} pk={self.pk}>"

    def __str__(self):
        return self.title


class Song(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.TextField(max_length=255, default="")
    artist = models.TextField(max_length=255, default="")
    album = models.TextField(max_length=255, default="")
    spotify_id = models.TextField(max_length=255, default="")
    spotify_uri = models.TextField(max_length=255, default="")
    apple_id = models.TextField(max_length=255, default="")
    preview_url = models.TextField(max_length=255, default="")
    mixtapes = models.ManyToManyField(Mixtape, related_name="songs", blank=True)

    def __repr__(self):
        return f"<Song title={self.title} pk={self.pk}>"

    def __str__(self):
        return self.title


# the following model can be added to create connections between users
# class Connection(models.Model):
#     created   = models.DateTimeField(auto_now_add=True, editable=False)
#     creator   = models.ForeignKey(User, related_name="friendship_creator_set")
#     following = models.ForeignKey(User, related_name="friend_set")
