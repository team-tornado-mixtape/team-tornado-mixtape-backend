from api.models import Mixtape, User, Profile, Song
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from api.serializers import (
    FollowingUpdateSerializer,
    MixtapeDetailSerializer,
    MixtapeListSerializer,
    ProfileSerializer,
    SongSerializer,
    Userserializer,
    UserFollowersSerializer,
    FavoriteMixtapeUpdateSerializer,
    MixtapeUpdateSerializer,
    MixtapeCreateSerializer,
)
from .custom_permissions import IsCreatorOrReadOnly, IsUserOrReadOnly
from django.views.generic.edit import CreateView
from django.db.models import Q, Count

from rest_framework.generics import ListCreateAPIView, ListAPIView, UpdateAPIView, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import (
    SAFE_METHODS,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)

from api.spotify_search import *
from api.apple_music_search import *
from api.helpers import *


class MixtapeViewSet(ModelViewSet):
    queryset = Mixtape.objects.all()
    serializer_class = MixtapeDetailSerializer
    permission_classes = [IsCreatorOrReadOnly]

    def get_serializer_class(self):
        if self.action in ["list"]:
            return MixtapeListSerializer
        elif self.action in ["create"]:
            return MixtapeCreateSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        search_term = self.request.query_params.get("search")
        if search_term is not None:
            results= Mixtape.objects.filter(
                Q(title__icontains=search_term)|
                Q(creator__username__icontains=search_term)
            )
        else:
            results = Mixtape.objects.all()
        return results
    
    def perform_create(self, serializer):
            serializer.save(creator=self.request.user)

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
            results= Profile.objects.filter(
                Q(user__username__icontains=search_term) |
                Q(user__first_name__icontains=search_term)|
                Q(user__last_name__icontains=search_term)
            )
        else:
            results = Profile.objects.annotate(total_mixtapes=Count('user__mixtapes'))
        return results

    def perform_create(self, serializer):
            serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        if self.request.user == instance.user:
            instance.delete()

    def perform_update(self, serializer):
        if self.request.user == serializer.instance.user:
            serializer.save()


class UserProfileView(ListCreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsUserOrReadOnly]

    def get_queryset(self):
        return Profile.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
            serializer.save(user=self.request.user)



class SongViewSet(ModelViewSet):
    queryset = Song.objects.all()
    serializer_class = SongSerializer

    def get_queryset(self):
        search_term = self.request.query_params.get("search")
        if search_term is not None:
            results= Song.objects.filter(
                Q(title__icontains=search_term) |
                Q(artist__icontains=search_term)
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


class MixtapeUpdateView(UpdateAPIView):
    queryset = Mixtape.objects.all()
    permission_classes = [IsCreatorOrReadOnly]
    serializer_class   = MixtapeUpdateSerializer

    def update(self, request, *args, **kwargs):
        mixtape_instance = Mixtape.objects.filter(pk=self.kwargs['mixtape_pk'])[0]
        song_instance = Song.objects.filter(pk=self.kwargs['song_pk'])[0]

        if song_instance not in mixtape_instance.songs.all():
            mixtape_instance.songs.add(song_instance)
        else:
            mixtape_instance.songs.remove(song_instance)

        serializer = self.get_serializer(mixtape_instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)


class CreateUpdateFollowingView(UpdateAPIView):
    queryset = Profile.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class   = FollowingUpdateSerializer

    def get_queryset(self):
        queryset = self.queryset
        return queryset.filter(pk=self.kwargs['profile_pk'])[0]

    def update(self, request, *args, **kwargs):
        instance = self.get_queryset()
        if self.request.user not in instance.followed_by.all():
            self.request.user.followers.add(instance)
        else:
            self.request.user.followers.remove(instance)

        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)


class CreateUpdateFavoriteView(UpdateAPIView):
    queryset = Mixtape.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class   = FavoriteMixtapeUpdateSerializer

    def get_queryset(self):
        queryset = self.queryset
        return queryset.filter(pk=self.kwargs['mixtape_pk'])[0]

    def update(self, request, *args, **kwargs):
        instance = self.get_queryset()
        if self.request.user not in instance.favorited_by.all():
            self.request.user.favorite_mixtapes.add(instance)
        else:
            self.request.user.favorite_mixtapes.remove(instance)

        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)


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



class DocumentCreateView(CreateView):
    model = Profile
    fields = ['image', ]
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        prorfiles = Profile.objects.all()
        context['profiles'] = profiles
        return context 


class SearchView(ListAPIView):
    permission_classes = [IsAuthenticated]
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

        songs = my_search(search_track=search_track, search_artist=search_artist, limit=limit)

        count = 0
        database_songs = Song.objects.all()
        queryset = Song.objects.none()

        for song in songs:
            if Song.objects.filter(spotify_uri=song['spotify_uri']).exists():
                queryset = queryset | Song.objects.filter(spotify_uri=song['spotify_uri'])
            else:
                count += 1
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

        return queryset | Song.objects.filter(user=self.request.user).order_by('-id')[:count]
