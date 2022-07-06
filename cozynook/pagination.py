from rest_framework import pagination


class MainPagination(pagination.PageNumberPagination):
    page_size_query_param = 'pageSize'
    page_query_param = 'current'
