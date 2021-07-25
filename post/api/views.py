from rest_framework.decorators import throttle_classes
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import (
                ListAPIView,
                RetrieveAPIView,
                DestroyAPIView,
                RetrieveUpdateAPIView,
                CreateAPIView,
            )

#IsOwner iznini biz yaztık çünkü update edilirken herkesin kendi objesini update etsin diye özel bir izin yazdık
from rest_framework.mixins import CreateModelMixin,DestroyModelMixin

from post.api.paginations import PostPagination
from post.api.permissions import IsOwner
from post.api.serializers import PostSerializer
from post.models import Post
from rest_framework.permissions import (
IsAuthenticated,
IsAdminUser,
)


"""
 def post(self,request,*args,**kwargs):
        return self.create(request,*args,**kwargs)

def perform_create(self, serializer):
        serializer.save(user = self.request.user)
        
        bunlar listapiviewa eklenerek aynı sayddfada hem list hem create işlemi de yapabilrsin tabi listpiviewin yanına 
        createmodelmixin i import etmen gerek
        
        yada aynı işleminn farklı yolu ise createmodelapi nin içine listmodelmixin i ekleyip def get handlerini yazabilirisin   

"""


#throtle scope str hatası veriyor normal throttle_classes kullan
class PostListAPIView(ListAPIView):
    # throttle_scope = 'hasan'
    serializer_class = PostSerializer
    filter_backends = [SearchFilter,OrderingFilter]
    search_fields = ['title','content']
    pagination_class = PostPagination

    def get_queryset(self):
        queryset = Post.objects.filter(draft=False)
        return queryset


class PostRetrieveAPIView(RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = "slug"


#default olarak lookup_field kısmı pk olarak geliyor yani oraya yazmana gerek yok sadece apideki urls.py de belirtsen yeter


# class PostDeleteAPIView(DestroyAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer
#     lookup_field = "slug"
#     permission_classes = [IsOwner]

#permissionclassesede virgül koyup istediğimiz kadar daha permisson ekleyebiliriz ama bu şartların hepsi sağlanırsa kullanıcıyı objeye erişecektir

class PostUpdateAPIView(RetrieveUpdateAPIView,DestroyModelMixin):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = "slug"
    permission_classes = [IsOwner]

    def perform_update(self, serializer):
        serializer.save(modified_by =self.request.user)

    def delete(self,request,*args,**kwargs):
        return self.destroy(request,*args,**kwargs)


class PostCreateAPIView(CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

#create yaparken sonuçta created date ve slug alanını kullanmayacazğız o yüzden modelde onların editableını false yaptık yani hem eklerken hemde
#update ederken bu alanları ssitem kendisi oluşturacaktırDiğer bir yöntem ise update ve create işlemleri için yeni bir serializer oluşturup field kısmına
#title content, image alanlarını yazmak olacaktır ve bu oluşturdupumuz serializeri ise api viewsda create ve update yaptığımız yerlerde serializerları
#değiştirmemiz gerkiyor