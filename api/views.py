from djoser.views import UserViewSet
from rest_framework import permissions

from users.models import User

from api.serializers import CustomUserSerializer


class UsersViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = (permissions.IsAuthenticated,)
