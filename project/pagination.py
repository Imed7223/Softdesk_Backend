from rest_framework.pagination import PageNumberPagination


class CustomPagination(PageNumberPagination):
    page_size = 10  # nombre d’éléments par page
    page_size_query_param = 'page_size'
    max_page_size = 100

