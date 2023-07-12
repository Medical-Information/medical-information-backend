from rest_framework.pagination import CursorPagination as CPagination


class CursorPagination(CPagination):
    ordering = '-created_at'
