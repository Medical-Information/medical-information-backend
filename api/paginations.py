from django.conf import settings
from rest_framework import pagination


class CursorPagination(pagination.CursorPagination):
    ordering = '-created_at'
    page_size = settings.CURSOR_PAGINATION_PAGE_SIZE
