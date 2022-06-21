from api.models import Mixtape
from rest_framework.viewsets import ModelViewSet
from api.serializers import MixtapeDetailSerializer,MixtapeListSerializer
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from .custom_permissions import IsCreatorOrReadOnly
from django.db.models import Count

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
        return Mixtape.objects.filter(responder_id=self.kwargs["creator_pk"])