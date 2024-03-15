from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomPagination(PageNumberPagination):

    page_size = 5
    # limit_query_param = "mylimit"
    page_size_query_param = "page_size"
    max_page_size = 5

    # def get_paginated_response(self, data):
    #     return Response(
    #         {
    #             "count": self.count,
    #             "next": self.get_next_link(),
    #             "previous": self.get_previous_link(),
    #             "results": data,
    #         }
    #     )
