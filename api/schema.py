from drf_spectacular.utils import extend_schema
from rest_framework import status

from api.serializers import (
    NotAuthenticatedSerializer,
    UserCreateSerializer,
    UserSerializer,
    ValidationSerializer,
)

USER_VIEW_SET_SCHEMA = {
    'list': extend_schema(
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
    'create': extend_schema(
        summary='Регистрация пользователя.',
        responses={
            status.HTTP_201_CREATED: UserCreateSerializer,
            status.HTTP_400_BAD_REQUEST: ValidationSerializer,
        },
    ),
    'activation': extend_schema(
        summary='Активация пользователя.',
        responses={
            status.HTTP_204_NO_CONTENT: None,
            status.HTTP_400_BAD_REQUEST: ValidationSerializer,
        },
    ),
    'resend_activation': extend_schema(
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
    'reset_password': extend_schema(
        summary='Смена пароля пользователя.',
        description=('Отправляется письмо со ссылкой для смены пароля.'),
        responses={
            status.HTTP_204_NO_CONTENT: None,
        },
    ),
    'reset_password_confirm': extend_schema(
        summary='Подтверждение смены пароля пользователя.',
        responses={
            status.HTTP_204_NO_CONTENT: None,
        },
    ),
    'set_password': extend_schema(
        summary='Смена пароля пользователем.',
        description=('Смена пароля пользователем при имеющейся авторизации.'),
        responses={
            status.HTTP_204_NO_CONTENT: None,
            status.HTTP_401_UNAUTHORIZED: NotAuthenticatedSerializer,
        },
    ),
}
