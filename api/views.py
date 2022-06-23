from api.models import Mixtape, User, Profile, Song
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from api.serializers import (
    MixtapeDetailSerializer,
    MixtapeListSerializer,
    ProfileSerializer,
    SongSerializer,
    Userserializer,
    SearchSerializer,
    )
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from .custom_permissions import IsCreatorOrReadOnly, IsUserOrReadOnly
from django.db.models import Count
from rest_framework.generics import ListAPIView
from api.spotify_search import *
from api.apple_music_search import *
from api.similar import *

# Create your views here.

class MixtapeViewSet(ModelViewSet):
    queryset           = Mixtape.objects.all()
    serializer_class   = MixtapeDetailSerializer
    permission_classes = [IsCreatorOrReadOnly]

    def get_serializer_class(self):
        if self.action in ["list"]:
            return MixtapeListSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        search_term = self.request.query_params.get("search")
        if search_term is not None:
            results = Mixtape.objects.filter(title__icontains=self.request.query_params.get("search"))
        else:
            results = Mixtape.objects.annotate(
                total_songs=Count('songs')
            )
        return results

    def perform_destroy(self, instance):
        if self.request.user  == instance.creator:
            instance.delete()

    def perform_update(self,serializer):
        if self.request.user == serializer.instance.creator:
            serializer.save()



class UserMixtapeListView(RetrieveUpdateDestroyAPIView):
    queryset           = Mixtape.objects.all()
    serializer_class   = MixtapeDetailSerializer
    permission_classes = [IsCreatorOrReadOnly]

    def get_queryset(self):
        return Mixtape.objects.filter(creator_id=self.kwargs["creator_pk"])


class UserViewSet(ReadOnlyModelViewSet):
    queryset            = User.objects.all()
    serializer_class    = Userserializer


class ProfileViewSet(ModelViewSet):
    queryset            = Profile.objects.all()
    serializer_class    = ProfileSerializer  
    permission_classes  = [IsUserOrReadOnly]

    def get_queryset(self):
        search_term = self.request.query_params.get("search")
        if search_term is not None:
            results = Profile.objects.filter(user__icontains=self.request.query_params.get("search"))
        else:
            results = Profile.objects.all()
        return results


class UserProfileView(RetrieveUpdateDestroyAPIView):
    queryset            = Profile.objects.all()
    serializer_class    = ProfileSerializer
    permission_classes  = [IsUserOrReadOnly]

    def get_queryset(self):
        return Profile.objects.filter(user_id=self.kwargs["user_pk"])



class SongViewSet(ModelViewSet):
    queryset            = Song.objects.all()
    serializer_class    = SongSerializer

    def perform_update(self, serializer):
        pass

    def perform_destroy(self, instance):
        pass


class SearchView(ListAPIView):
    serializer_class = SongSerializer

    def get_queryset(self):
        search_term = self.request.query_params.get('search')
        spotify_results = SearchSpotifyAPI(search_term)
        apple_results = SearchAppleMusicAPI(search_term)
        songs = []

        for i in range(len(spotify_results)):
            similarities = []
            for j in range(len(apple_results)):
                similarity = similar(spotify_results[i]['spotify_title'], apple_results[j]['apple_title']) + similar(spotify_results[i]['spotify_artist'], apple_results[j]['apple_artist'])
                similarities.append(similarity)

            closest = max(similarities)

            if closest > 0.8:
                index = similarities.index(closest)
                song = {'title': apple_results[index]['apple_title'], 'artist': apple_results[index]['apple_artist'], 'album': apple_results[index]['apple_album'], 'spotify_id': spotify_results[index]['spotify_id'], 'apple_id': apple_results[index]['apple_id']}

                songs.append(song)

        for song in range(len(songs)):
            Song.objects.create(title=songs[i]['title'], artist=songs[i]['artist'], album=songs[i]['album'], spotify_id=songs[i]['spotify_id'], apple_id=songs[i]['apple_id'])

        breakpoint()
        return songs
