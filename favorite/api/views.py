from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from comment.api.permissions import IsOwner
from favorite.api.paginations import FavoritePagination
from favorite.api.serializers import FavoriteListCreateAPISerializer, FavoriteAPISerializer
from favorite.models import (
    Favourite,
)

#get queryset kullandık çünkü  filtre yaptık

class FavoriteListCreateAPIView(ListCreateAPIView):
    # queryset = Favourite.objects.all()
    serializer_class = FavoriteListCreateAPISerializer
    pagination_class = FavoritePagination
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return Favourite.objects.filter(user = self.request.user)

    def perform_create(self, serializer):
        serializer.save(user = self.request.user)



class FavoriteAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Favourite.objects.all()
    serializer_class = FavoriteAPISerializer
    lookup_field = "pk"
    permission_classes = [IsOwner]




