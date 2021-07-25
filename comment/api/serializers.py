from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from comment.models import Comment
from post.models import Post


class CommentCreateSerializer(ModelSerializer):
    class Meta:
        model = Comment
        exclude = ["created",]

    def validate(self, attrs):
        if attrs["parent"]:
            if attrs["parent"].post != attrs["post"]:
                raise serializers.ValidationError("Something went wrong")
        return attrs


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'last_name' , 'email')


class PostSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'title',)


class CommentListSerializer(ModelSerializer):
    user = UserSerializer()
    post = PostSerializer()
    class Meta:
        model = Comment
        fields = "__all__"


    def get_replies(self,obj):
        if obj.any_children:
            return CommentListSerializer(obj.children(),many=True).data



#seralizerin sonuna .data yazarak serializerden veriyi alabailiriz


class CommentDeleteUpdateSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = (
            "content",
        )
