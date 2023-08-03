from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdmin(BasePermission):
    """Разрешает доступ только для администраторов."""

    message = 'Необходимы права администратора.'

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.is_admin
            or request.user.is_superuser
        )

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)


class IsAuthor(BasePermission):
    """Разрешает доступ только для автора."""
    message = ''

    def has_permission(self, request, view):
        self.message = 'Необходима авторизация.'
        return request.method in SAFE_METHODS or request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        self.message = 'Необходимо авторство.'
        return request.user == obj.user


class ReadOnly(BasePermission):
    """Разрешает доступ на чтение."""

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)
