from django.contrib.auth import get_user_model
from djoser.serializers import UserSerializer as DjoserUserSerializer
from drf_extra_fields.fields import Base64ImageField
from rest_framework.serializers import (
    BooleanField,
    ModelSerializer,
    SerializerMethodField,
)

from articles.models import Article, Tag

User = get_user_model()


class UserSimpleSerializer(DjoserUserSerializer):
    """Сериализатор модели User для сериализатора модели Article."""

    class Meta:
        model = User
        fields = [
            'id',
            'first_name',
            'last_name',
            'role',
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


class TagSubtreeSerializer(TagSimpleSerializer):
    class Meta(TagSimpleSerializer.Meta):
        pass

    def get_fields(self) -> dict:
        fields = super(TagSubtreeSerializer, self).get_fields()
        fields['children'] = TagSubtreeSerializer(many=True, required=False)
        return fields


class ArticleSerializer(ModelSerializer):
    is_fan = SerializerMethodField()
    is_hater = SerializerMethodField()
    total_likes = SerializerMethodField()
    total_dislikes = SerializerMethodField()
    rating = SerializerMethodField()
    image = Base64ImageField()
    is_favorited = BooleanField(read_only=True)
    author = UserSimpleSerializer(read_only=True)
    tags = TagSimpleSerializer(many=True, read_only=True)

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
