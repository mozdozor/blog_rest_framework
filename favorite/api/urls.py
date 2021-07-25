from django.urls import path, include
from .views import (
FavoriteListCreateAPIView,FavoriteAPIView
)

app_name = "favorite"

urlpatterns = [
     path('list-create', FavoriteListCreateAPIView.as_view(), name="list-create"),
     path('update/<pk>', FavoriteAPIView.as_view(), name="update"),
    # path('update/<pk>', CommentUpdateAPIView.as_view(), name="update"),



]


