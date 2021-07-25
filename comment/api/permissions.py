from rest_framework.permissions import BasePermission

#adminse veya kullanıcının kendi yazısı ise erişsin dedik

class IsOwner(BasePermission):

    #has permission sürekli çalışır ve tetiklenir
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    message = "You must be the owner of this object"

    # has object permission ise sadece kullanıcının kendi postu oldupunda çalışır
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user



