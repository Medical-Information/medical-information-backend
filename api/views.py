from django.contrib.auth import get_user_model
from djoser.views import UserViewSet as UViewSet
from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet

from api.filters import ArticleTextSearchFilter
from api.permissions import IsAdmin, ReadOnly
from api.serializers import ArticleSerializer, UserSerializer
from articles.models import Article

User = get_user_model()


class UserViewSet(UViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)


class ArticleViewSet(ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [ReadOnly | IsAdmin]  # [AllowAny]  for debug
    filter_backends = [ArticleTextSearchFilter]
    search_fields = ['text']
