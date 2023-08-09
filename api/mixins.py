from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.permissions import LikesIsNotObjectOwner
from articles.models import Viewer
from core.utils import get_client_ip
from likes import services
from likes.models import VoteTypes


class LikedMixin:
    @action(
        methods=['POST'],
        detail=True,
        url_path='vote/(?P<vote_type>\\w+)',
        permission_classes=(IsAuthenticated & LikesIsNotObjectOwner,),
    )
    def add_vote(self, request, pk=None, vote_type=None):
        """Добавляет лайк или дизлайк в зависимости от vote_type."""
        votes = {'like': VoteTypes.LIKE, 'dislike': VoteTypes.DISLIKE}
        obj = self.get_object()
        if vote_type not in votes:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        services.add_vote(obj, request.user, votes[vote_type])
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        methods=['POST'],
        detail=True,
        permission_classes=(IsAuthenticated & LikesIsNotObjectOwner,),
    )
    def unvote(self, request, pk=None):
        """Удаляет голос (лайк/дизлайк)."""
        obj = self.get_object()
        services.remove_vote(obj, request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)


class CountViewerMixin:
    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        instance = self.get_object()
        if hasattr(instance, 'viewers'):  # noqa: WPS110
            viewer, created = Viewer.objects.get_or_create(
                ipaddress=None
                if request.user.is_authenticated
                else get_client_ip(request),
                user=request.user if request.user.is_authenticated else None,
            )

            if not instance.viewers.filter(id=viewer.id).exists():
                instance.viewers.add(viewer)

        return response
