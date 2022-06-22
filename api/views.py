from api.models import Mixtape, User, Profile, Song
from rest_framework.viewsets import ModelViewSet,ReadOnlyModelViewSet
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView
from api.serializers import MixtapeDetailSerializer,MixtapeListSerializer, ProfileSerializer, SongSerializer, Userserializer
from .custom_permissions import IsCreatorOrReadOnly, IsUserOrReadOnly

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
            results = Mixtape.objects.all()
        return results

    def perform_destroy(self, instance):
        if self.request.user  == instance.creator:
            instance.delete()

    def perform_update(self,serializer):
        if self.request.user == serializer.instance.creator:
            serializer.save()



class UserMixtapeListView(ListCreateAPIView):
    queryset           = Mixtape.objects.all()
    serializer_class   = MixtapeListSerializer
    permission_classes = [IsCreatorOrReadOnly]
    
    def get_queryset(self):
        return Mixtape.objects.filter(creator=self.request.user)
    

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


class UserProfileView(ListCreateAPIView):
    queryset            = Profile.objects.all()
    serializer_class    = ProfileSerializer
    permission_classes  = [IsUserOrReadOnly]

    def get_queryset(self):
        return Profile.objects.filter(user=self.request.user)



class SongViewSet(ModelViewSet):
    queryset            = Song.objects.all()
    serializer_class    = SongSerializer

    def perform_update(self, serializer):
        pass

    def perform_destroy(self, instance):
        pass
