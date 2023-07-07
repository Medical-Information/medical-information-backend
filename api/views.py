from djoser.views import UserViewSet as UViewSet
from rest_framework import permissions

from users.models import User

from api.serializers import UserSerializer


class UserViewSet(UViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)
