from django.contrib.auth import get_user_model
from django.db.models import Exists, OuterRef, Q, Sum, Value
from django.db.models.functions import Coalesce
from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import TokenCreateView as DjoserTokenCreateView
from djoser.views import TokenDestroyView as DjoserTokenDestroyView
from djoser.views import UserViewSet as DjoserUserViewSet
from drf_spectacular.utils import extend_schema_view
from rest_framework import filters, status
from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from api import schema
from api.filters import ArticleFilter
from api.mixins import LikedMixin
from api.paginations import CursorPagination
from api.permissions import ArticleOwnerPermission, IsAdmin, IsAuthor, ReadOnly
from api.serializers import (
    ArticleCreateSerializer,
    ArticleSerializer,
    CommentSerializer,
    DummySerializer,
    TagRootsSerializer,
    TagSerializer,
    TagSubtreeSerializer,
)
from articles.models import Article, FavoriteArticle, Tag
from likes.models import Vote, VoteTypes
from likes.utils import annotate_user_queryset

User = get_user_model()


@extend_schema_view(**schema.TOKEN_CREATE_VIEW_SCHEMA)
class TokenCreateView(DjoserTokenCreateView):
    pass


@extend_schema_view(**schema.TOKEN_DESTROY_VIEW_SCHEMA)
class TokenDestroyView(DjoserTokenDestroyView):
    serializer_class = DummySerializer


@extend_schema_view(**schema.USER_VIEW_SET_SCHEMA)
class UserViewSet(DjoserUserViewSet):
    # отключаем смену логина (email)
    reset_username = None
    reset_username_confirm = None
    # отключаем установку логина (email)
    set_username = None

    def get_queryset(self) -> QuerySet:
        queryset = super().get_queryset()
        return annotate_user_queryset(queryset)

    def get_instance(self):
        return self.get_queryset().get(pk=self.request.user.pk)

    # переопределил, так как родительский метод зачем-то отправляет письмо на активацию
    def perform_update(self, serializer):
        serializer.save()

    @action(
        methods=['PATCH', 'DELETE'],
        detail=False,
        permission_classes=(IsAuthenticated,),
    )
    def subscription(self, request):
        if (
            request.user.subscribed
            and request.method == 'PATCH'
            or not request.user.subscribed
            and request.method == 'DELETE'
        ):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        request.user.subscribed = request.method == 'PATCH'
        request.user.save(update_fields=('subscribed',))
        return Response(
            status=status.HTTP_204_NO_CONTENT,
        )


@extend_schema_view(**schema.ARTICLE_VIEW_SET_SCHEMA)
class ArticleViewSet(LikedMixin, ReadOnlyModelViewSet, CreateModelMixin):
    serializer_class = ArticleSerializer
    pagination_class = CursorPagination
    permission_classes = (IsAuthenticatedOrReadOnly & ArticleOwnerPermission,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_class = ArticleFilter
    search_fields = (
        'title',
        'text',
        'source_name',
        'author__first_name',
        'author__last_name',
    )

    def get_queryset(self):
        qs = (
            Article.objects.filter(is_published=True)
            .select_related('author')
            .prefetch_related('tags', 'votes')
            .annotate(rating=Coalesce(Sum('votes__vote'), 0))
            .annotate(
                likes_count=Coalesce(Sum('votes__vote', filter=Q(votes__vote__gt=0)), 0),
            )
            .annotate(
                dislikes_count=Coalesce(
                    Sum('votes__vote', filter=Q(votes__vote__lt=0)),
                    0,
                ),
            )
        )

        user = self.request.user
        if user.is_authenticated:
            user_votes = Vote.objects.filter(user=user, object_id=OuterRef('pk'))
            qs = (
                qs.annotate(
                    is_favorited=Exists(
                        FavoriteArticle.objects.filter(
                            article=OuterRef('pk'),
                            user=user,
                        ),
                    ),
                )
                .annotate(is_fan=Exists(user_votes.filter(vote=VoteTypes.LIKE)))
                .annotate(is_hater=Exists(user_votes.filter(vote=VoteTypes.DISLIKE)))
            )
        else:
            qs = (
                qs.annotate(is_favorited=Value(False))
                .annotate(is_fan=Value(False))
                .annotate(is_hater=Value(False))
            )
        return qs.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return ArticleCreateSerializer
        return ArticleSerializer

    @action(
        methods=['post', 'delete'],
        detail=True,
        permission_classes=(IsAuthenticated,),
    )
    def favorite(self, request, pk):
        if request.method == 'POST':
            return self._create_favorite(request, pk)

        if request.method == 'DELETE':
            return self._delete_favorite(request, pk)

    def _create_favorite(self, request, pk):
        article = get_object_or_404(self.get_queryset(), pk=pk)
        fav_article, is_created = FavoriteArticle.objects.get_or_create(
            article=article,
            user=request.user,
        )
        if is_created:
            serializer = self.get_serializer(self.get_object())
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(
            {'non_field_errors': _('Article is favorited already.')},
            status.HTTP_400_BAD_REQUEST,
        )

    def _delete_favorite(self, request, pk):
        article = get_object_or_404(self.get_queryset(), pk=pk)
        favorited = FavoriteArticle.objects.filter(
            article=article,
            user=request.user,
        )
        if favorited.exists():
            favorited.delete()
            serializer = self.get_serializer(self.get_object())
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(
            {'non_field_errors': _('Article is not favorited yet.')},
            status.HTTP_400_BAD_REQUEST,
        )


@extend_schema_view(**schema.TAG_VIEW_SET_SCHEMA)
class TagViewSet(ReadOnlyModelViewSet):
    queryset = Tag.objects.select_related('parent').prefetch_related('children')
    serializer_class = TagSerializer

    @action(detail=False)
    def roots(self, request) -> Response:
        all_roots = self.get_queryset().filter(parent__isnull=True)
        serializer = TagRootsSerializer(all_roots, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @action(detail=True)
    def subtree(self, request, pk) -> Response:
        tag = self.get_queryset().filter(pk=pk)
        serializer = TagSubtreeSerializer(tag, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class CommentViewSet(ModelViewSet):  # feature. LikedMixin
    serializer_class = CommentSerializer
    permission_classes = (IsAdmin | IsAuthor | ReadOnly,)

    def get_queryset(self):
        article = get_object_or_404(Article, id=self.kwargs.get('article_id'))
        new_queryset = article.comments.all().select_related('author')
        return new_queryset

    def perform_create(self, serializer):
        article = get_object_or_404(Article, id=self.kwargs.get('article_id'))
        serializer.save(author=self.request.user, article=article)
