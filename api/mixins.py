from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.serializers import UserSerializer
from likes import services
from likes.models import LikeDislike


class LikedMixin:
    @action(
        methods=['POST'],
        detail=True,
        url_path='vote/(?P<vote_type>\\w+)',
        permission_classes=(IsAuthenticated,),
    )
    def vote(self, request, pk=None, vote_type=None):
        """Добавляет лайк или дизлайк в зависимости от vote_type."""
        votes = {'like': LikeDislike.LIKE, 'dislike': LikeDislike.DISLIKE}
        obj = self.get_object()
        if vote_type not in votes:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        services.add_vote(obj, request.user, votes[vote_type])
        return Response()

    @action(
        methods=['POST'],
        detail=True,
        permission_classes=(IsAuthenticated,),
    )
    def unvote(self, request, pk=None):
        """Удаляет голос (лайк/дизлайк)."""
        obj = self.get_object()
        services.remove_vote(obj, request.user)
        return Response()

    @action(
        methods=['GET'],
        detail=True,
        url_path='votes/(?P<votes_group>\\w+)',
    )
    def votes(self, request, pk=None, votes_group=None):
        """Возвращает всех пользователей, голосовавших по объекту."""
        votes = {'fans': LikeDislike.LIKE, 'haters': LikeDislike.DISLIKE}
        obj = self.get_object()
        if votes_group not in votes:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        users = services.get_voters_by_object(obj, votes[votes_group])
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
