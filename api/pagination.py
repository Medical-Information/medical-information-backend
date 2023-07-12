from rest_framework.pagination import CursorPagination


class CursorPagination(CursorPagination):
    ordering = '-created_at'
