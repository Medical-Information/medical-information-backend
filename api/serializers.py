from django.conf import settings
from django.contrib.auth import get_user_model
from djoser.serializers import ActivationSerializer as DjoserActivationSerializer
from djoser.serializers import UserSerializer as DjoserUserSerializer
from drf_extra_fields.fields import Base64ImageField
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import (
    BooleanField,
    CharField,
    CurrentUserDefault,
    HiddenField,
    ListField,
    ModelSerializer,
    Serializer,
    SerializerMethodField,
)

from api.validators import (
    ImageBytesSizeValidator,
    ImageContentTypeValidator,
    ImageDimensionValidator,
)
from articles.models import Article, Comment, Tag

User = get_user_model()


class ActivationSerializer(DjoserActivationSerializer):
    def validate(self, attrs):
        # костыли для защиты от "дурака"
        if not isinstance(self.initial_data.get('uid'), str):
            key_error = 'invalid_uid'
            raise ValidationError(
                {'uid': [self.error_messages[key_error]]},
                code=key_error,
            )
        if not isinstance(self.initial_data.get('token'), str):
            key_error = 'invalid_token'
            raise ValidationError(
                {'token': [self.error_messages[key_error]]},
                code=key_error,
            )

        return super().validate(attrs)


class UserCreateSerializer(DjoserUserSerializer):
    pass


class UserSimpleSerializer(DjoserUserSerializer):
    """Сериализатор модели User для сериализатора модели Article."""

    avatar = Base64ImageField(
        validators=(
            ImageBytesSizeValidator(settings.BASE64_AVATAR_MAX_SIZE_BYTES),
            ImageDimensionValidator(
                settings.BASE64_AVATAR_MAX_WIDTH,
                settings.BASE64_AVATAR_MAX_HEIGHT,
            ),
            ImageContentTypeValidator(settings.ALLOWED_B64ENCODED_IMAGE_FORMATS),
        ),
    )

    class Meta:
        model = User
        fields = [
            'id',
            'first_name',
            'last_name',
            'role',
            'avatar',
        ]


class UserSerializer(UserSimpleSerializer):
    """Полный сериализатор модели User."""

    rating = SerializerMethodField()
    publications_amount = SerializerMethodField()

    class Meta(UserSimpleSerializer.Meta):
        model = User
        fields = UserSimpleSerializer.Meta.fields + [
            'email',
            'rating',
            'publications_amount',
            'subscribed',
        ]
        read_only_fields = ('subscribed', 'email', 'role')

    def get_rating(self, user) -> int:
        return user.rating

    def get_publications_amount(self, user) -> int:
        return user.publications_amount


class TagSimpleSerializer(ModelSerializer):
    """Сериализатор для списка тегов в сериализаторе модели Article."""

    class Meta:
        model = Tag
        fields = [
            'pk',
            'name',
        ]


class TagRootsSerializer(ModelSerializer):
    """Сериализатор для корневых тегов, модель Tag."""

    children = TagSimpleSerializer(many=True, required=False)

    class Meta(TagSimpleSerializer.Meta):
        fields = TagSimpleSerializer.Meta.fields + [
            'children',
        ]


class TagSerializer(TagRootsSerializer):
    """Полный сериализатор тегов, модель Tag."""

    parent = TagSimpleSerializer(required=False)

    class Meta(TagRootsSerializer.Meta):
        fields = TagRootsSerializer.Meta.fields + [
            'parent',
        ]


class CommentSerializer(ModelSerializer):
    author = UserSimpleSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = (
            'id',
            'text',
            'author',
            'created_at',
            'updated_at',
        )
        read_only_fields = ('id', 'author', 'created_at', 'updated_at')


class ArticleSerializer(ModelSerializer):
    is_fan = SerializerMethodField()
    is_hater = SerializerMethodField()
    total_likes = SerializerMethodField()
    total_dislikes = SerializerMethodField()
    rating = SerializerMethodField()
    views_count = SerializerMethodField()
    image = Base64ImageField()
    is_favorited = BooleanField(read_only=True)
    author = UserSimpleSerializer(read_only=True)
    tags = TagSimpleSerializer(many=True, read_only=True)
    comments = CommentSerializer(read_only=True, many=True)

    class Meta:
        model = Article
        fields = (
            'id',
            'is_fan',
            'is_hater',
            'total_likes',
            'total_dislikes',
            'rating',
            'image',
            'is_favorited',
            'created_at',
            'updated_at',
            'title',
            'annotation',
            'text',
            'source_name',
            'source_link',
            'is_published',
            'views_count',
            'author',
            'tags',
            'comments',
        )
        read_only_fields = ('created_at', 'updated_at')

    def get_is_fan(self, obj) -> bool:
        return obj.is_fan

    def get_is_hater(self, obj) -> bool:
        return obj.is_hater

    def get_total_likes(self, obj) -> int:
        return obj.likes_count

    def get_total_dislikes(self, obj) -> int:
        return obj.dislikes_count

    def get_rating(self, obj) -> int:
        return obj.rating

    def get_views_count(self, obj) -> int:
        return obj.views_count


class ValidationSerializer(Serializer):
    """HTTP_400."""

    property_1 = CharField()
    property_2 = CharField()
    non_field_errors = ListField()


class DetailSerializer(Serializer):
    detail = CharField()


class NotAuthenticatedSerializer(DetailSerializer):
    """HTTP_401."""

    pass


class NotFoundSerializer(DetailSerializer):
    """HTTP_404."""

    pass


class DummySerializer(Serializer):
    """Заглушка для drf-spectacular, чтобы не ругался ViewSet без сериализаторов."""

    pass


class ArticleCreateSerializer(ModelSerializer):
    image = Base64ImageField(
        validators=(
            ImageBytesSizeValidator(settings.BASE64_IMAGE_MAX_SIZE_BYTES),
            ImageContentTypeValidator(settings.ALLOWED_B64ENCODED_IMAGE_FORMATS),
        ),
    )
    author = HiddenField(default=CurrentUserDefault())

    class Meta:
        model = Article
        fields = (
            'author',
            'title',
            'annotation',
            'text',
            'source_name',
            'source_link',
            'image',
        )

    def to_representation(self, instance):
        """Предполагается, после создания статья имеет начальные значения атрибутов."""
        instance.is_fan = False
        instance.is_hater = False
        instance.likes_count = 0
        instance.dislikes_count = 0
        instance.rating = 0
        instance.views_count = 0
        return ArticleSerializer().to_representation(instance)
