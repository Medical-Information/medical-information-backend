from django.contrib.auth import get_user_model
from django.db.models import Exists, OuterRef, Q, Sum, Value
from django.db.models.functions import Coalesce
from django.db.models.query import QuerySet
from django.utils.translation import gettext_lazy as _
from django_filters.rest_framework import DjangoFilterBackend
from djoser import serializers as djoser_serializers
from djoser.views import TokenCreateView as DjoserTokenCreateView
from djoser.views import TokenDestroyView as DjoserTokenDestroyView
from djoser.views import UserViewSet as DjoserUserViewSet
from drf_spectacular.utils import OpenApiExample, extend_schema, extend_schema_view
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from api.filters import ArticleFilter
from api.mixins import LikedMixin
from api.paginations import CursorPagination
from api.permissions import IsAdmin, ReadOnly
from api.serializers import (
    ArticleSerializer,
    DummySerializer,
    NotAuthenticatedSerializer,
    TagRootsSerializer,
    TagSerializer,
    TagSubtreeSerializer,
    UserCreateSerializer,
    UserSerializer,
    ValidationSerializer,
)
from articles.models import Article, FavoriteArticle, Tag
from likes.models import Vote, VoteTypes
from likes.utils import annotate_user_queryset

User = get_user_model()


@extend_schema_view(
    post=extend_schema(
        summary='Аутентификация пользователя.',
        description='При успешной аутентификации возвращается токен.',
        responses={
            status.HTTP_200_OK: djoser_serializers.TokenSerializer,
            status.HTTP_400_BAD_REQUEST: ValidationSerializer,
        },
        examples=[
            OpenApiExample(
                'Example',
                request_only=True,
                value={'email': 'user@example.com', 'password': 'password'},
            ),
        ],
    ),
)
class TokenCreateView(DjoserTokenCreateView):
    pass


@extend_schema_view(
    post=extend_schema(
        summary='Отзыв аутентификации пользователя.',
        description='При успешном отзыве аутентификации удаляется токен.',
        responses={
            status.HTTP_204_NO_CONTENT: None,
            status.HTTP_401_UNAUTHORIZED: NotAuthenticatedSerializer,
        },
    ),
)
class TokenDestroyView(DjoserTokenDestroyView):
    serializer_class = DummySerializer


@extend_schema_view(
    list=extend_schema(
        summary='Получение списка пользователей.',
        description=(
            'Всех пользователей получает только персонал портала. '
            'Обычный пользователь получает только себя.'
        ),
        responses={
            status.HTTP_200_OK: UserSerializer,
            status.HTTP_401_UNAUTHORIZED: NotAuthenticatedSerializer,
        },
    ),
    create=extend_schema(
        summary='Регистрация пользователя.',
        responses={
            status.HTTP_201_CREATED: UserCreateSerializer,
            status.HTTP_400_BAD_REQUEST: ValidationSerializer,
        },
    ),
    activation=extend_schema(
        summary='Активация пользователя.',
        responses={
            status.HTTP_204_NO_CONTENT: None,
            status.HTTP_400_BAD_REQUEST: ValidationSerializer,
        },
    ),
    resend_activation=extend_schema(
        summary='Реактивация пользователя.',
        description=(
            'Сбрасывается признак активации пользователя и '
            'запускается процесс активации пользователя.'
        ),
        responses={
            status.HTTP_204_NO_CONTENT: None,
            status.HTTP_400_BAD_REQUEST: ValidationSerializer,
        },
    ),
    reset_password=extend_schema(
        summary='Смена пароля пользователя.',
        description=('Отправляется письмо со ссылкой для смены пароля.'),
        responses={
            status.HTTP_204_NO_CONTENT: None,
        },
    ),
    reset_password_confirm=extend_schema(
        summary='Подтверждение смены пароля пользователя.',
        responses={
            status.HTTP_204_NO_CONTENT: None,
        },
    ),
    set_password=extend_schema(
        summary='Смена пароля пользователем.',
        description=('Смена пароля пользователем при имеющейся авторизации.'),
        responses={
            status.HTTP_204_NO_CONTENT: None,
            status.HTTP_401_UNAUTHORIZED: NotAuthenticatedSerializer,
        },
    ),
)
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


class ArticleViewSet(LikedMixin, ModelViewSet):
    serializer_class = ArticleSerializer
    pagination_class = CursorPagination
    permission_classes = (IsAdmin | ReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ArticleFilter

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
        return Response(
            {'errors': _('Article is not favorited yet.')},
            status.HTTP_400_BAD_REQUEST,
        )


class TagViewSet(ReadOnlyModelViewSet):
    """Вьюсет модели Tag."""

    queryset = Tag.objects.prefetch_related('parent', 'children').all()
    serializer_class = TagSerializer

    @action(detail=False)
    def roots(self, request) -> Response:
        all_roots = self.get_queryset().filter(parent__isnull=True)
        serializer = TagRootsSerializer(all_roots, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @action(detail=True)
    def subtree(self, request, pk) -> Response:
        tag = Tag.objects.filter(pk=pk)
        serializer = TagSubtreeSerializer(tag, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
