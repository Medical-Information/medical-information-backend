from rest_framework.decorators import action
from rest_framework.response import Response

from likes import services
from api.serializers import UserSerializer


class LikedMixin:
    @action(methods=['POST'], detail=True)
    def like(self, request, pk=None):
        """Лайкает `obj`.
        """
        obj = self.get_object()
        services.add_like(obj, request.user)
        return Response()

    @action(methods=['POST'], detail=True)
    def unlike(self, request, pk=None):
        """Удаляет лайк с `obj`.
        """
        obj = self.get_object()
        services.remove_like(obj, request.user)
        return Response()

    @action(methods=['GET'], detail=True)
    def fans(self, request, pk=None):
        """Получает всех пользователей, которые лайкнули `obj`.
        """
        obj = self.get_object()
        fans = services.get_fans(obj)
        serializer = UserSerializer(fans, many=True)
        return Response(serializer.data)

    @action(methods=['POST'], detail=True)
    def dislike(self, request, pk=None):
        """Дизлайкает `obj`.
        """
        obj = self.get_object()
        services.add_like(obj, request.user)
        return Response()

    @action(methods=['POST'], detail=True)
    def undislike(self, request, pk=None):
        """Удаляет дизлайк с `obj`.
        """
        obj = self.get_object()
        services.remove_like(obj, request.user)
        return Response()

    @action(methods=['GET'], detail=True)
    def haters(self, request, pk=None):
        """Получает всех пользователей, которые дизлайкнули `obj`.
        """
        obj = self.get_object()
        fans = services.get_fans(obj)
        serializer = FanSerializer(fans, many=True)
        return Response(serializer.data)
