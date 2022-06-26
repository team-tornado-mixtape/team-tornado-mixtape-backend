from rest_framework import serializers
from .models import Mixtape, Profile, Song, User


class MixtapeDetailSerializer(serializers.ModelSerializer):
    creator = serializers.SlugRelatedField(read_only=True, slug_field="username")
    songs   = serializers.SlugRelatedField(read_only=True, slug_field="title", many=True)
    favorited_by = serializers.SlugRelatedField(read_only=True, slug_field="username",many=True)


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
            "favorite_count"
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
    # user = serializers.SlugRelatedField(read_only=True, slug_field="username")
    followed_by = serializers.SlugRelatedField(read_only=True, slug_field="username",many=True)
    class Meta:
        model = Profile
        fields = [
                "id",
                "get_username",
                "followed_by",
                "image",
                "follower_count",
                "get_first_name",
                "get_last_name",
                "mixtape_count"
                ]



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
            "first_name",
            "last_name",
        ]


class SongSerializer(serializers.ModelSerializer):
    mixtape = serializers.SlugRelatedField(read_only=True, slug_field="title")

    class Meta:
        model = Song
        fields = "__all__"


class FavoriteMixtapeUpdateSerializer(serializers.ModelSerializer):
        class Meta:
            model = Mixtape
            fields= [
                "title",
            ]

class FollowingUpdateSerializer(serializers.ModelSerializer):

        class Meta:
            model = Profile
            fields= [
                "get_username",
            ]
