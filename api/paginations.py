from django.conf import settings
from rest_framework import pagination


class CursorPagination(pagination.CursorPagination):
    ordering = '-created_at'
    page_size = settings.CURSOR_PAGINATION_PAGE_SIZE
    page_size_query_param = 'page_size'
    max_page_size = settings.CURSOR_PAGINATION_MAX_PAGE_SIZE
