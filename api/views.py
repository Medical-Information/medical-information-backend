from django.contrib.auth import get_user_model
from djoser.views import UserViewSet as UViewSet
from rest_framework.viewsets import ModelViewSet
from api.mixins import LikedMixin
from api.filters import ArticleTextSearchFilter
from api.permissions import IsAdmin, ReadOnly
from api.serializers import ArticleSerializer, UserSerializer
from articles.models import Article

User = get_user_model()


class UserViewSet(UViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ArticleViewSet(LikedMixin, ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = (ReadOnly | IsAdmin,)  # (permissions.AllowAny,)  for debug
    filter_backends = (ArticleTextSearchFilter,)
    search_fields = ('text',)
