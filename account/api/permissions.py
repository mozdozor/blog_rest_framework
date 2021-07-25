from rest_framework.permissions import BasePermission

#adminse veya kullanıcının kendi yazısı ise erişsin dedik

class notAuthenticated(BasePermission):

    #has permission sürekli çalışır ve tetiklenir sizi içeri bile sokmaz has_object_permisson sizi içeri sokar ama yinede oda oluşturmaz
    def has_permission(self, request, view):
        return not request.user.is_authenticated

    message = "You have already an account"



