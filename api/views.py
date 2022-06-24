from api.models import Mixtape, User, Profile, Song
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from api.serializers import (
    MixtapeDetailSerializer,
    MixtapeListSerializer,
    ProfileSerializer,
    SongSerializer,
    Userserializer,
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
        # sourcery skip: assign-if-exp, inline-immediately-returned-variable, lift-return-into-if
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


class ProfileViewSet(ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsUserOrReadOnly]

    def get_queryset(self):
        search_term = self.request.query_params.get("search")
        if search_term is not None:
            results = Profile.objects.filter(
                user__username=self.request.query_params.get("search")
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

    def perform_create(self,serializer):
        pass

    def perform_update(self, serializer):
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


class SearchView(ListAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = SongSerializer

    def get_queryset(self):
        Song.objects.filter(mixtapes=None).delete()

        search_term = self.request.query_params.get("search")
        spotify_results = SearchSpotifyAPI(search_term)
        apple_results = SearchAppleMusicAPI(search_term)
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
                }

                songs.append(song)

        for i in range(len(songs)):
            Song.objects.create(
                title=songs[i]["title"],
                artist=songs[i]["artist"],
                album=songs[i]["album"],
                spotify_id=songs[i]["spotify_id"],
                apple_id=songs[i]["apple_id"],
            )

        return Song.objects.all().order_by("-id")[: len(songs)]
