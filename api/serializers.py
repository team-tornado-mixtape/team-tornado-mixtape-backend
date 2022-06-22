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
        fields = ['id','title','created_at','creator',]


class ProfileSerializer(serializers.ModelSerializer):
    user   = serializers.SlugRelatedField(read_only=True, slug_field="username")

    class Meta:
        model  = Profile
        fields = ('__all__')
        

class Userserializer(serializers.ModelSerializer):

    class Meta:
        model  = User
        fields = ['id','username',]


class SongSerializer(serializers.ModelSerializer):
    mixtape   = serializers.SlugRelatedField(read_only=True, slug_field='title')
    
    class Meta:
        model = Song
        fields = ('__all__')