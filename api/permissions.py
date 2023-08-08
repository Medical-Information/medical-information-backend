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


class ReadOnly(BasePermission):
    """Разрешает доступ на чтение."""

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)


class ArticleOwnerPermission(BasePermission):
    """Разрешает доступ к статье администратору или её автору."""

    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS or request.user == obj.author


class LikesIsNotObject0wner(BasePermission):
    """Запрещает ставить лайки/дизлайки своим собственным объектам."""

    def has_permission(self, request, view):
        obj = view.get_object()
        return not (request.user == obj.author)
