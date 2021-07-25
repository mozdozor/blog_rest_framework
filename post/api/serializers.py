from rest_framework import serializers
from post.models import Post


# post objesinin içerisindeki göstermek istediğimiz verilerin adlarını yazıyoruz aynı olmak zorunda object adı ile


class PostSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name = "post:detail",
        lookup_field = "slug"
    )
    username = serializers.SerializerMethodField("get_username")
    username2 = serializers.SerializerMethodField("get_username2")
    class Meta:
        model = Post
        fields = (
            "username",
            "title",
            "content",
            "image",
            "url",
            "created",
            "username2",
        )
    def get_username(self, obj):
        return obj.user.username
    def get_username2(self, obj):
        if obj.modified_by is not None:
            return obj.modified_by.username


"""

normal serializer uğraştırır bu

class PostSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=200)
    content = serializers.CharField(max_length=200)


"""
