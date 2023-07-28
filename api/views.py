from django.contrib.auth import get_user_model
from django.db.models import Exists, OuterRef, Value
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
    @action(
        methods=['PATCH', 'DELETE'],
        detail=False,
        permission_classes=(IsAuthenticated,),
    )
    def subscription(self, request):
        user = User.objects.get(pk=request.user.id)
        if request.method == 'PATCH':
            if user.subscriber:
                return Response(
                    {'error': 'You are already subscribed to the newsletter'},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            user.subscriber = True
            user.save()
            return Response(
                {'error': 'You have subscribed to the newsletter'},
                status=status.HTTP_201_CREATED,
            )
        else:
            if not user.subscriber:
                return Response(
                    {'error': 'You are not subscribed to the newsletter'},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            user.subscriber = False
            user.save()
            return Response(
                {'error': 'You have unsubscribed from the newsletter'},
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

    queryset = Tag.objects.all()
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
