from rest_framework.pagination import PageNumberPagination


#bu classsı direkt views içerisindede ayzabilridik ama daha derli toplu olmaı açısından burada yazdık

class CommentPagination(PageNumberPagination):
    page_size = 2