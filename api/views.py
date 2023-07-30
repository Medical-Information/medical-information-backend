from django.contrib.auth import get_user_model
from django.db.models import Count, Exists, OuterRef, Sum, Value
from django.db.models.functions import Coalesce
from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from django_filters.rest_framework import DjangoFilterBackend
from djoser.serializers import TokenSerializer
from djoser.views import TokenCreateView as DjoserTokenCreateView
from djoser.views import TokenDestroyView as DjoserTokenDestroyView
from djoser.views import UserViewSet as DjoserUserViewSet
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
from api.serializers import ArticleSerializer, TagRootsSerializer, TagSerializer
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


class UserViewSet(DjoserUserViewSet):
    def get_queryset(self) -> QuerySet:
        return (
            User.objects.annotate(rating=Coalesce(Sum('likes__vote'), 0))
            .annotate(publications_amount=Count('articles', distinct=True))
            .all()
        )

    def get_instance(self):
        return self.get_queryset().get(pk=self.request.user.pk)

    @action(
        methods=['PATCH', 'DELETE'],
        detail=False,
        permission_classes=(IsAuthenticated,),
    )
    def subscription(self, request):
        user = User.objects.get(pk=request.user.id)
        if (
            user.subscribed
            and request.method == 'PATCH'
            or not user.subscribed
            and request.method == 'DELETE'
        ):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        if request.method == 'PATCH':
            user.subscribed = True
            user.save()
            return Response(
                status=status.HTTP_201_CREATED,
            )
        else:
            user.subscribed = False
            user.save()
            return Response(
                status=status.HTTP_204_NO_CONTENT,
            )


class ArticleViewSet(LikedMixin, ModelViewSet):
    serializer_class = ArticleSerializer
    pagination_class = CursorPagination
    permission_classes = (IsAdmin | ReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ArticleFilter

    def get_queryset(self):
        qs = Article.objects.filter(is_published=True).select_related('author')

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
        if FavoriteArticle.objects.get_or_create(
            article_id=pk,
            user=request.user,
        )[1]:
            return Response(status=status.HTTP_201_CREATED)
        get_object_or_404(Article, id=pk)
        return Response(
            {'errors': _('Article is favorited already.')},
            status.HTTP_400_BAD_REQUEST,
        )

    @favorite.mapping.delete
    def delete_favorite(self, request, pk):
        if FavoriteArticle.objects.filter(
            article_id=pk,
            user=request.user,
        ).delete()[0]:
            return Response(status=status.HTTP_204_NO_CONTENT)
        get_object_or_404(Article, id=pk)
        return Response(
            {'errors': _('Article is not favorited yet.')},
            status.HTTP_400_BAD_REQUEST,
        )


class TagViewSet(ReadOnlyModelViewSet):
    """Вьюсет модели Tag."""

    queryset = Tag.objects.prefetch_related('parent', 'children').all()
    serializer_class = TagSerializer

    def get_serializer(self, *args, **kwargs):
        if self.action == 'roots':
            return TagRootsSerializer(*args, **kwargs)
        return super().get_serializer(*args, **kwargs)

    @action(detail=False)
    def roots(self, request):
        all_roots = self.get_queryset().filter(parent__isnull=True)
        serializer = self.get_serializer(all_roots, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
