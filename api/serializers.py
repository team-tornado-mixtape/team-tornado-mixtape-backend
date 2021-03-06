from rest_framework import serializers
from .models import Mixtape, Profile, Song, User, Image


class SongSerializer(serializers.ModelSerializer):
    # mixtape = serializers.SlugRelatedField(read_only=True, slug_field="title")

    class Meta:
        model = Song
        fields = "__all__"


class MixtapeDetailSerializer(serializers.ModelSerializer):
    creator = serializers.SlugRelatedField(read_only=True, slug_field="username")
    songs = SongSerializer(many=True)
    favorited_by = serializers.SlugRelatedField(
        read_only=True, slug_field="username", many=True
    )

    class Meta:
        model = Mixtape
        fields = [
            "id",
            "title",
            "created_at",
            "creator",
            "description",
            "theme",
            "is_public",
            "modified_at",
            "favorited_by",
            "favorite_count",
            "songs",
        ]


class MixtapeListSerializer(serializers.ModelSerializer):
    creator = serializers.SlugRelatedField(read_only=True, slug_field="username")
    songs = SongSerializer(many=True)
    favorited_by = serializers.SlugRelatedField(
        read_only=True, slug_field="username", many=True
    )

    class Meta:
        model = Mixtape
        fields = [
            "id",
            "title",
            "created_at",
            "creator",
            "description",
            "theme",
            "is_public",
            "modified_at",
            "favorited_by",
            "favorite_count",
            "songs",
        ]


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = "__all__"
        lookup_field = "pk"


class ImagePostPutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = [
            "picture",
        ]


class ProfileSerializer(serializers.ModelSerializer):
    followed_by = serializers.SlugRelatedField(
        read_only=True, slug_field="username", many=True
    )
    total_mixtapes = serializers.IntegerField(read_only=True)
    images = ImagePostPutSerializer(many=True)

    class Meta:
        model = Profile
        fields = [
            "id",
            "get_user_id",
            "get_username",
            "get_first_name",
            "get_last_name",
            "followed_by",
            "follower_count",
            "total_mixtapes",
            "spotify_username",
            "apple_username",
            "images",
        ]


class UserFollowersSerializer(serializers.ModelSerializer):
    followed_by = serializers.SlugRelatedField(
        read_only=True, slug_field="username", many=True
    )

    class Meta:
        model = Profile
        fields = ["followed_by"]


class Userserializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
        ]


class FavoriteMixtapeUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mixtape
        fields = [
            "title",
        ]


class FollowingUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            "get_username",
        ]


class MixtapeUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mixtape
        fields = [
            "songs",
        ]


class MixtapeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mixtape
        fields = [
            "id",
            "title",
        ]


class ProfilePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            "id",
            "get_user_id",
            "get_username",
            "get_first_name",
            "get_last_name",
            "spotify_username",
            "apple_username",
        ]
