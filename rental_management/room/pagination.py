from rest_framework.pagination import LimitOffsetPagination


class CustomPagination(LimitOffsetPagination):
    default_limit = 5
    # limit_query_param = "mylimit"
    offset_query_param = "skip"
    max_limit = 5
