from rest_framework import serializers
from .models import Mixtape, Profile, Song, User


class MixtapeDetailSerializer(serializers.ModelSerializer):
    creator = serializers.SlugRelatedField(read_only=True, slug_field="username")
    
    class Meta:
        model = Mixtape
        fields = [
            "created_at",
            "creator",
            "title",
            "songs",
            "theme",
            "is_public",
            "description",
            "modified_at",
            "favorited_by",
        ]


class MixtapeListSerializer(serializers.ModelSerializer):
    creator = serializers.SlugRelatedField(read_only=True, slug_field="username")
    songs   = serializers.SlugRelatedField(read_only=True, slug_field="title", many=True)

    class Meta:
        model = Mixtape
        fields = [
            "id",
            "title",
            "created_at",
            "creator",
            "songs",
        ]


class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(read_only=True, slug_field="username")
    followed_by = serializers.SlugRelatedField(read_only=True, slug_field="username",many=True)
    class Meta:
        model = Profile
        fields = "__all__"


class UserFollowersSerializer(serializers.ModelSerializer):
    followed_by = serializers.SlugRelatedField(read_only=True, slug_field="username",many=True)
    class Meta:
        model  = Profile
        fields = ["followed_by"]



class Userserializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
        ]


class SongSerializer(serializers.ModelSerializer):
    mixtape = serializers.SlugRelatedField(read_only=True, slug_field="title")

    class Meta:
        model = Song
        fields = "__all__"
