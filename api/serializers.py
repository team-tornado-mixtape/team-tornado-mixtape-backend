from dataclasses import fields
from rest_framework import serializers 
from .models import Mixtape, Profile,Song, User


class MixtapeDetailSerializer(serializers.ModelSerializer):
    creator   = serializers.SlugRelatedField(read_only=True, slug_field="username")

    class Meta:
        model  = Mixtape
        fields = ('__all__')

class MixtapeListSerializer(serializers.ModelSerializer):
    creator   = serializers.SlugRelatedField(read_only=True, slug_field="username")

    class Meta:
        model  = Mixtape
        fields = ['id','title','created_at']

