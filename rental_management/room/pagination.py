from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response


class CustomPagination(LimitOffsetPagination):

    default_limit = 15
    # limit_query_param = "mylimit"
    offset_query_param = "skip"
    max_limit = 5

    # def get_paginated_response(self, data):
    #     return Response(
    #         {
    #             "count": self.count,
    #             "next": self.get_next_link(),
    #             "previous": self.get_previous_link(),
    #             "results": data,
    #         }
    #     )
