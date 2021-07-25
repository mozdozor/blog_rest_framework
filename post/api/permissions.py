from rest_framework.permissions import BasePermission

#adminse veya kullanıcının kendi yazısı ise erişsin dedik

class IsOwner(BasePermission):

    #has permission sürekli çalışır ve tetiklenir
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    message = "You must be the owner of this object"

    # has object permission ise sadece kullanıcının kendi postu oldupunda çalışır
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user or request.user.is_superuser






#base permissson clasında birde has_permission var o da has objectten önce çalışır yani kullanıcı giriş yapmışmı onu
#kontrol eder eğer kullanıcı giriş yapmamışsa atıyorum başkasının postu için apilerde delete butonu bile gelmez ama onu yazmassak sadece
#has object permisson yazarsak delete butonu gelir fakat yine delete yapamaz