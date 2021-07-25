from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView, get_object_or_404, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import update_session_auth_hash

from account.api.permissions import notAuthenticated
from account.api.serializers import UserSerializer, ChangePasswordSerializer, RegisterSerializer
from account.api.throttles import RegisterThrottle


class ProfileView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset,id=self.request.user.id)
        return obj

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)



class UpdatePassword(APIView):
    permission_classes = [IsAuthenticated,]

    #get object demesende olurdu put fonksiyonunda get_object çağırmka yerine direkt self.request.user da diyebilirsin sadece daha güzel görünmesi açıısndan yaptık
    def get_object(self):
        return self.request.user

    def put(self,request,*args,**kwargs):
        self.object=self.get_object()

        # data ={
        #     "old_password":request.data["old_password"],
        #     "new_password": request.data["new_password"]
        #
        # }
        # serializer=ChangePasswordSerializer(data=data)    böylede olabilir ama aşağıda yazdığım daha kısa ve mantıklı bşr yöntem
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            old_password=serializer.data.get("old_password")
            if not self.object.check_password(old_password):
                return Response({"old_password":"wrong_password"},status=status.HTTP_400_BAD_REQUEST)

            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            update_session_auth_hash(request, request.user)
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class CreateUserView(CreateAPIView):
    ##saatte 5 post işemi yapsın dedik botları engellemek için throttle ile
    throttle_classes = [RegisterThrottle,]
    model = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [notAuthenticated,]