from djoser import serializers as djoser_serializers
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiExample, OpenApiParameter, extend_schema
from rest_framework import status

from api.serializers import (
    ArticleCreateSerializer,
    ArticleSerializer,
    NotAuthenticatedSerializer,
    UserCreateSerializer,
    UserSerializer,
    ValidationSerializer,
)

ARTICLE_VIEW_SET_SCHEMA = {
    'list': extend_schema(
        summary='Получить список статей.',
    ),
    'create': extend_schema(
        summary='Создать статью.',
        request=ArticleCreateSerializer,
        responses={
            status.HTTP_201_CREATED: ArticleSerializer,
            status.HTTP_400_BAD_REQUEST: ValidationSerializer,
            status.HTTP_401_UNAUTHORIZED: NotAuthenticatedSerializer,
        },
    ),
    'retrieve': extend_schema(
        summary='Получить информацию о статье.',
        parameters=[
            OpenApiParameter(
                name='id',
                type=OpenApiTypes.UUID,
                location=OpenApiParameter.PATH,
                description='Идентификатор статьи (UUID).',
            ),
        ],
    ),
    'post_favorite': {
        extend_schema(
            summary='Добавить в избранное.',
            request=None,
            parameters=[
                OpenApiParameter(
                    name='id',
                    type=OpenApiTypes.UUID,
                    location=OpenApiParameter.PATH,
                    description='Идентификатор статьи (UUID).',
                ),
            ],
            responses={
                status.HTTP_204_NO_CONTENT: None,
                status.HTTP_401_UNAUTHORIZED: NotAuthenticatedSerializer,
            },
        ),
    },
    'delete_favorite': {
        extend_schema(
            summary='Удалить из избранного.',
            request=None,
            parameters=[
                OpenApiParameter(
                    name='id',
                    type=OpenApiTypes.UUID,
                    location=OpenApiParameter.PATH,
                    description='Идентификатор статьи (UUID).',
                ),
            ],
            responses={
                status.HTTP_204_NO_CONTENT: None,
                status.HTTP_401_UNAUTHORIZED: NotAuthenticatedSerializer,
            },
        ),
    },
    'unvote': extend_schema(
        summary='Убрать оценку у статьи.',
        request=None,
        parameters=[
            OpenApiParameter(
                name='id',
                type=OpenApiTypes.UUID,
                location=OpenApiParameter.PATH,
                description='Идентификатор статьи (UUID).',
            ),
        ],
        responses={
            status.HTTP_204_NO_CONTENT: None,
            status.HTTP_400_BAD_REQUEST: ValidationSerializer,
            status.HTTP_401_UNAUTHORIZED: NotAuthenticatedSerializer,
        },
    ),
    'add_vote': extend_schema(
        summary='Поставить оценку статье.',
        request=None,
        parameters=[
            OpenApiParameter(
                name='id',
                type=OpenApiTypes.UUID,
                location=OpenApiParameter.PATH,
                description='Идентификатор статьи (UUID).',
            ),
            OpenApiParameter(
                name='vote_type',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.PATH,
                description='Тип оценки (like/dislike).',
            ),
        ],
        responses={
            status.HTTP_204_NO_CONTENT: None,
            status.HTTP_400_BAD_REQUEST: ValidationSerializer,
            status.HTTP_401_UNAUTHORIZED: NotAuthenticatedSerializer,
        },
    ),
}

TOKEN_CREATE_VIEW_SCHEMA = {
    'post': extend_schema(
        summary='Авторизовать пользователя.',
        description='При успешной авторизации возвращается токен.',
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
}


TOKEN_DESTROY_VIEW_SCHEMA = {
    'post': extend_schema(
        summary='Отозвать авторизацию пользователя.',
        description='При успешном отзыве авторизацию удаляется токен.',
        responses={
            status.HTTP_204_NO_CONTENT: None,
            status.HTTP_401_UNAUTHORIZED: NotAuthenticatedSerializer,
        },
    ),
}


USER_VIEW_SET_SCHEMA = {
    'list': extend_schema(
        summary='Получить список пользователей.',
        description=(
            'Всех пользователей получает только персонал портала. '
            'Обычный пользователь получает только себя.'
        ),
        responses={
            status.HTTP_200_OK: UserSerializer,
            status.HTTP_401_UNAUTHORIZED: NotAuthenticatedSerializer,
        },
    ),
    'create': extend_schema(
        summary='Зарегистрировать пользователя.',
        responses={
            status.HTTP_201_CREATED: UserCreateSerializer,
            status.HTTP_400_BAD_REQUEST: ValidationSerializer,
        },
    ),
    'retrieve': extend_schema(
        summary='Получить информацию о пользователе.',
        parameters=[
            OpenApiParameter(
                name='id',
                type=OpenApiTypes.UUID,
                location=OpenApiParameter.PATH,
                description='Идентификатор пользователя (UUID).',
            ),
        ],
        responses={
            status.HTTP_200_OK: UserSerializer,
            status.HTTP_401_UNAUTHORIZED: NotAuthenticatedSerializer,
        },
    ),
    'update': extend_schema(
        summary='Изменить информацию о пользователе.',
        parameters=[
            OpenApiParameter(
                name='id',
                type=OpenApiTypes.UUID,
                location=OpenApiParameter.PATH,
                description='Идентификатор пользователя (UUID).',
            ),
        ],
        responses={
            status.HTTP_200_OK: UserSerializer,
            status.HTTP_400_BAD_REQUEST: ValidationSerializer,
            status.HTTP_401_UNAUTHORIZED: NotAuthenticatedSerializer,
        },
    ),
    'partial_update': extend_schema(
        summary='Частично изменить информацию о пользователе.',
        parameters=[
            OpenApiParameter(
                name='id',
                type=OpenApiTypes.UUID,
                location=OpenApiParameter.PATH,
                description='Идентификатор пользователя (UUID).',
            ),
        ],
        responses={
            status.HTTP_200_OK: UserSerializer,
            status.HTTP_400_BAD_REQUEST: ValidationSerializer,
            status.HTTP_401_UNAUTHORIZED: NotAuthenticatedSerializer,
        },
    ),
    'destroy': extend_schema(
        summary='Удалить пользователя.',
        parameters=[
            OpenApiParameter(
                name='id',
                type=OpenApiTypes.UUID,
                location=OpenApiParameter.PATH,
                description='Идентификатор пользователя (UUID).',
            ),
        ],
        responses={
            status.HTTP_204_NO_CONTENT: None,
            status.HTTP_401_UNAUTHORIZED: NotAuthenticatedSerializer,
        },
    ),
    'activation': extend_schema(
        summary='Активировать пользователя.',
        description=(
            'Поля uid и token требуется взять из ссылки, '
            'отправленной пользователю на почту.'
        ),
        responses={
            status.HTTP_204_NO_CONTENT: None,
            status.HTTP_400_BAD_REQUEST: ValidationSerializer,
        },
    ),
    'me': {
        extend_schema(
            methods=['get'],
            summary='Получить информацию о пользователе.',
            description='Используется текущий (авторизованный) пользователь.',
            responses={
                status.HTTP_200_OK: UserSerializer,
                status.HTTP_401_UNAUTHORIZED: NotAuthenticatedSerializer,
            },
        ),
        extend_schema(
            methods=['put'],
            summary='Изменить информацию о пользователе.',
            description='Используется текущий (авторизованный) пользователь.',
            responses={
                status.HTTP_200_OK: UserSerializer,
                status.HTTP_400_BAD_REQUEST: ValidationSerializer,
                status.HTTP_401_UNAUTHORIZED: NotAuthenticatedSerializer,
            },
        ),
        extend_schema(
            methods=['patch'],
            summary='Частично изменить информацию о пользователе.',
            description='Используется текущий (авторизованный) пользователь.',
            responses={
                status.HTTP_200_OK: UserSerializer,
                status.HTTP_400_BAD_REQUEST: ValidationSerializer,
                status.HTTP_401_UNAUTHORIZED: NotAuthenticatedSerializer,
            },
        ),
        extend_schema(
            methods=['delete'],
            summary='Удалить пользователя.',
            description='Используется текущий (авторизованный) пользователь.',
            responses={
                status.HTTP_204_NO_CONTENT: None,
                status.HTTP_401_UNAUTHORIZED: NotAuthenticatedSerializer,
            },
        ),
    },
    'resend_activation': extend_schema(
        summary='Повторить активацию пользователя.',
        description=(
            'Сбрасывается признак активации пользователя и '
            'процесс активации запускается заново.'
        ),
        responses={
            status.HTTP_204_NO_CONTENT: None,
            status.HTTP_400_BAD_REQUEST: ValidationSerializer,
        },
    ),
    'reset_password': extend_schema(
        summary='Сменить пароль пользователя (восстановление доступа).',
        description='Отправляется письмо со ссылкой для смены пароля.',
        responses={
            status.HTTP_204_NO_CONTENT: None,
        },
    ),
    'reset_password_confirm': extend_schema(
        summary='Подтвердить смену пароля пользователя.',
        description=(
            'Поля uid и token требуется взять из ссылки, '
            'отправленной пользователю на почту.'
        ),
        responses={
            status.HTTP_204_NO_CONTENT: None,
        },
    ),
    'set_password': extend_schema(
        summary='Сменить пароль пользователя.',
        description=('Смена пароля пользователем при имеющейся авторизации.'),
        responses={
            status.HTTP_204_NO_CONTENT: None,
            status.HTTP_401_UNAUTHORIZED: NotAuthenticatedSerializer,
        },
    ),
    'subscription': {
        extend_schema(
            methods=['patch'],
            summary='Подписаться на почтовую рассылку.',
            responses={
                status.HTTP_204_NO_CONTENT: None,
                status.HTTP_401_UNAUTHORIZED: NotAuthenticatedSerializer,
            },
        ),
        extend_schema(
            methods=['delete'],
            summary='Удалить подписку на почтовую рассылку.',
            responses={
                status.HTTP_204_NO_CONTENT: None,
                status.HTTP_401_UNAUTHORIZED: NotAuthenticatedSerializer,
            },
        ),
    },
}


TAG_VIEW_SET_SCHEMA = {
    'list': extend_schema(
        summary='Получить список всех тегов.',
    ),
    'retrieve': extend_schema(
        summary='Получить информацию о теге.',
        parameters=[
            OpenApiParameter(
                name='id',
                type=OpenApiTypes.UUID,
                location=OpenApiParameter.PATH,
                description='Идентификатор тега (UUID).',
            ),
        ],
    ),
    'subtree': extend_schema(
        summary='Получить все дочерние теги по указанному.',
        parameters=[
            OpenApiParameter(
                name='id',
                type=OpenApiTypes.UUID,
                location=OpenApiParameter.PATH,
                description='Идентификатор тега (UUID).',
            ),
        ],
    ),
    'roots': extend_schema(
        summary='Получить корневые теги.',
    ),
}
