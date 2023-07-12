from django.contrib.auth import get_user_model
from django.db.models import Exists, OuterRef, Value
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet as UViewSet
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from api.filters import ArticleFilter
from api.permissions import IsAdmin, ReadOnly
from api.serializers import ArticleSerializer, UserSerializer
from articles.models import Article, FavoriteArticle

User = get_user_model()


class UserViewSet(UViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


@method_decorator(
    name='list',
    decorator=swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'is_favorited',
                openapi.IN_QUERY,
                description=_('Is favorited article'),
                type=openapi.TYPE_BOOLEAN,
            ),
        ],
    ),
)
class ArticleViewSet(ModelViewSet):
    serializer_class = ArticleSerializer
    permission_classes = (ReadOnly | IsAdmin,)  # (permissions.AllowAny,)  for debug
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ArticleFilter

    def get_queryset(self):
        qs = Article.objects.all()

        user = self.request.user
        # вычисляем is_favorited - является ли статья избранной для пользователя
        if user.is_authenticated:
            is_favorited_expression = Exists(
                FavoriteArticle.objects.filter(article=OuterRef('pk'), user=user),
            )
        else:
            is_favorited_expression = Value(False)
        qs = qs.annotate(is_favorited=is_favorited_expression)

        return qs

    @action(methods=['post'], detail=True, permission_classes=(IsAuthenticated,))
    def favorite(self, request, pk):
        article = get_object_or_404(Article, id=pk)
        if FavoriteArticle.objects.filter(article=article, user=request.user).exists():
            return Response(
                {'errors': _('Article is favorited already.')},
                status.HTTP_400_BAD_REQUEST,
            )
        instance = FavoriteArticle(article=article, user=request.user)
        instance.save()
        return Response(status=status.HTTP_201_CREATED)

    @favorite.mapping.delete
    def delete_favorite(self, request, pk):
        article = get_object_or_404(Article, id=pk)
        if not FavoriteArticle.objects.filter(
            article=article,
            user=request.user,
        ).exists():
            return Response(
                {'errors': _('Article is not favorited yet.')},
                status.HTTP_400_BAD_REQUEST,
            )
        FavoriteArticle.objects.filter(article=article, user=request.user).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
