from django.urls import path, include
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from .views import (
                PostListAPIView,
                PostRetrieveAPIView,
                # PostDeleteAPIView,
                PostUpdateAPIView,
                PostCreateAPIView,
                )

app_name = "post"

urlpatterns = [
    path('list', cache_page(60*1)(PostListAPIView.as_view()), name="list"),
    path('detail/<slug>', PostRetrieveAPIView.as_view(), name="detail"),
    # path('delete/<slug>', PostDeleteAPIView.as_view(), name="delete"),
    path('update/<slug>', PostUpdateAPIView.as_view(), name="update"),
    path('create', PostCreateAPIView.as_view(), name="create"),

]

#cache_page veirileri önbelleğe alır kullanııc isteğine göre eğer önvbellekte varsa hemen getiri ama yoksa tekrar veritabanı sorgusu yapar