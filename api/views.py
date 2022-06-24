from api.models import Mixtape, User, Profile, Song
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from api.serializers import (
    MixtapeDetailSerializer,
    MixtapeListSerializer,
    ProfileSerializer,
    SongSerializer,
    Userserializer,
    UserFollowersSerializer,
)
from .custom_permissions import IsCreatorOrReadOnly, IsUserOrReadOnly
from django.db.models import Count

from rest_framework.generics import ListCreateAPIView, ListAPIView, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import (
    SAFE_METHODS,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)

from api.spotify_search import *
from api.apple_music_search import *
from api.similar import *


# Create your views here.


class MixtapeViewSet(ModelViewSet):
    queryset = Mixtape.objects.all()
    serializer_class = MixtapeDetailSerializer
    permission_classes = [IsCreatorOrReadOnly]

    def get_serializer_class(self):
        if self.action in ["list"]:
            return MixtapeListSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        search_term = self.request.query_params.get("search")
        if search_term is not None:
            results = Mixtape.objects.filter(
                title__icontains=self.request.query_params.get("search")
            )
        else:
            results = Mixtape.objects.all()
        return results

    def perform_destroy(self, instance):
        if self.request.user == instance.creator:
            instance.delete()

    def perform_update(self, serializer):
        if self.request.user == serializer.instance.creator:
            serializer.save()


class UserMixtapeListView(ListCreateAPIView):
    queryset = Mixtape.objects.all()
    serializer_class = MixtapeListSerializer
    permission_classes = [IsCreatorOrReadOnly]

    def get_queryset(self):
        return Mixtape.objects.filter(creator=self.request.user)


class UserViewSet(ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = Userserializer
    permission_classes = [IsAuthenticated]



class ProfileViewSet(ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsUserOrReadOnly]

    def get_queryset(self):
        search_term = self.request.query_params.get("search")
        if search_term is not None:
            results = Profile.objects.filter(
                user__username__icontains=self.request.query_params.get("search")
            )
        else:
            results = Profile.objects.all()
        return results


class UserProfileView(ListCreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsUserOrReadOnly]

    def get_queryset(self):
        return Profile.objects.filter(user=self.request.user)


class SongViewSet(ModelViewSet):
    queryset = Song.objects.all()
    serializer_class = SongSerializer

    def get_queryset(self):
        search_term = self.request.query_params.get("search")
        if search_term is not None:
            results = Song.objects.filter(
                title__icontains=self.request.query_params.get("search")
            )
        else:
            results = Song.objects.all()
        return results

    def perform_create(self,serializer):
        pass

    def update(self, serializer):
    #only allowed to update which mixtape the song is in
        pass

    def perform_destroy(self, instance):
        pass


class CreateFollowerView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, **kwargs):
        user = self.request.user
        profile = get_object_or_404(Profile, pk=self.kwargs["profile_pk"])
        user.followers.add(profile)
        serializer = ProfileSerializer(profile, context={"request": request})
        return Response(serializer.data, status=201)


class CreateFavoriteView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class   = MixtapeDetailSerializer

    def post(self, request, **kwargs):
        user = self.request.user
        mixtape = get_object_or_404(Mixtape, pk=self.kwargs["mixtape_pk"])
        user.favorite_mixtapes.add(mixtape)
        serializer = MixtapeDetailSerializer(
            mixtape, context={"request": request}
        )
        return Response(serializer.data, status=201)


class FavoriteMixtapeListView(ListAPIView):
    queryset         = Mixtape.objects.all()
    serializer_class = MixtapeListSerializer

    def get_queryset(self):
        return self.request.user.favorite_mixtapes.all()


class UserFollowingView(ListAPIView):
    queryset         = Profile.objects.all
    serializer_class = ProfileSerializer

    def get_queryset(self):
        return self.request.user.followers.all()


class UserFollowersView(ListAPIView):
    queryset         = Profile.objects.all
    serializer_class = UserFollowersSerializer

    def get_queryset(self):
        return Profile.objects.filter(user=self.request.user)    



class SearchView(ListAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = SongSerializer

    def get_queryset(self):
        Song.objects.filter(mixtapes=None, user=self.request.user).delete()

        if  self.request.query_params.get("track") is not None:
            search_track = self.request.query_params.get("track")
        else:
            search_track = None

        if  self.request.query_params.get("artist") is not None:
            search_artist = self.request.query_params.get("artist")
        else:
            search_artist = None

        if  self.request.query_params.get("limit") is not None:
            limit = self.request.query_params.get("limit")
        else:
            limit = 20

        spotify_results = SearchSpotifyAPI(search_track=search_track, search_artist=search_artist, limit=limit)
        apple_results = SearchAppleMusicAPI(search_track=search_track, search_artist=search_artist, limit=limit)
        songs = []

        for i in range(len(spotify_results)):
            similarities = []
            for j in range(len(apple_results)):
                similarity = similar(
                    spotify_results[i]["spotify_title"], apple_results[j]["apple_title"]
                ) + similar(
                    spotify_results[i]["spotify_artist"],
                    apple_results[j]["apple_artist"],
                )
                similarities.append(similarity)

            closest = max(similarities)

            if closest > 1.1:
                index = similarities.index(closest)
                song = {
                    "title": apple_results[index]["apple_title"],
                    "artist": apple_results[index]["apple_artist"],
                    "album": apple_results[index]["apple_album"],
                    "spotify_id": spotify_results[index]["spotify_id"],
                    "apple_id": apple_results[index]["apple_id"],
                    "spotify_uri": spotify_results[index]["spotify_uri"],
                    "preview_url": apple_results[index]["apple_preview_url"],
                }

                songs.append(song)

        for song in songs:
            Song.objects.create(
                user=self.request.user,
                title=song["title"],
                artist=song["artist"],
                album=song["album"],
                spotify_id=song["spotify_id"],
                apple_id=song["apple_id"],
                spotify_uri=song["spotify_uri"],
                preview_url=song["preview_url"],
                )

        return Song.objects.filter(user=self.request.user).order_by('-id')[:len(songs)]
