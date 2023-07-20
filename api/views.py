from django.contrib.auth import get_user_model
from django.db.models import Exists, OuterRef, Value
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from django_filters.rest_framework import DjangoFilterBackend
from djoser.serializers import TokenSerializer
from djoser.views import TokenCreateView as DjoserTokenCreateView
from djoser.views import TokenDestroyView as DjoserTokenDestroyView
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from api.filters import ArticleFilter
from api.mixins import LikedMixin
from api.paginations import CursorPagination
from api.permissions import IsAdmin, ReadOnly
from api.serializers import ArticleSerializer, TagSerializer
from articles.models import Article, FavoriteArticle, Tag

User = get_user_model()


@extend_schema_view(
    post=extend_schema(
        description='create token',
        responses={status.HTTP_200_OK: TokenSerializer},
    ),
)
class TokenCreateView(DjoserTokenCreateView):
    pass


@extend_schema_view(
    post=extend_schema(
        description='destroy token',
        responses={status.HTTP_204_NO_CONTENT: None},
    ),
)
class TokenDestroyView(DjoserTokenDestroyView):
    pass


class ArticleViewSet(LikedMixin, ModelViewSet):
    serializer_class = ArticleSerializer
    pagination_class = CursorPagination
    permission_classes = (IsAdmin | ReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ArticleFilter

    def get_queryset(self):
        qs = Article.objects.all()

        user = self.request.user
        if user.is_authenticated:
            is_favorited_expression = Exists(
                FavoriteArticle.objects.filter(
                    article=OuterRef('pk'),
                    user=user,
                ),
            )
        else:
            is_favorited_expression = Value(False)
        qs = qs.annotate(is_favorited=is_favorited_expression)

        return qs

    @action(
        methods=['post'],
        detail=True,
        permission_classes=(IsAuthenticated,),
    )
    def favorite(self, request, pk):
        article = get_object_or_404(Article, id=pk)
        if FavoriteArticle.objects.filter(
            article=article,
            user=request.user,
        ).exists():
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
        FavoriteArticle.objects.filter(
            article=article,
            user=request.user,
        ).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TagViewSet(ReadOnlyModelViewSet):
    """Tag ViewSet."""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer

    @action(detail=False)
    def roots(self, request):
        all_roots = self.get_queryset().filter(parent__isnull=True)
        serializer = TagSerializer(all_roots, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
