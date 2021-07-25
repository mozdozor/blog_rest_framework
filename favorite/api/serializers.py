from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from favorite.models import Favourite


class FavoriteListCreateAPISerializer(ModelSerializer):
    class Meta:
        model = Favourite
        fields = "__all__"

    def validate(self, attrs):
        query = Favourite.objects.filter(post = attrs["post"] ,user = attrs["user"])
        if query:
            raise serializers.ValidationError("This post has been added before")
        return attrs



class FavoriteAPISerializer(ModelSerializer):
    class Meta:
        model = Favourite
        fields = ("content",)
