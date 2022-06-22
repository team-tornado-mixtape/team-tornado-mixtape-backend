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
        fields = ['id','title','created_at','total_songs']


class ProfileSerializer(serializers.ModelSerializer):
    user   = serializers.SlugRelatedField(read_only=True, slug_field="username")

    class Meta:
        model  = Profile
        fields = ('__all__')
        

class Userserializer(serializers.ModelSerializer):
    user = serializers.SlugField(read_only=True, slug_field="username")

    class Meta:
        model  = User
        fields = ('__all__')