from django.contrib.auth import get_user_model
from djoser.serializers import UserSerializer as DjoserUserSerializer
from drf_extra_fields.fields import Base64ImageField
from rest_framework.serializers import (
    BooleanField,
    ModelSerializer,
    SerializerMethodField,
)

from articles.models import Article, Tag
from likes import services as likes_services
from likes.models import Vote
from users import services as users_services

User = get_user_model()


class UserSerializer(DjoserUserSerializer):
    rating = SerializerMethodField()
    publications_amount = SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'first_name',
            'last_name',
            'rating',
            'publications_amount',
        )

    def get_rating(self, user) -> int:
        return users_services.get_rating(user)

    def get_publications_amount(self, user) -> int:
        return users_services.get_publications_amount(user)


class UserCreateSerializer(DjoserUserSerializer):
    class Meta:
        model = User
        fields = (
            'email',
            'password',
            'first_name',
            'last_name',
        )
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class ArticleSerializer(ModelSerializer):
    is_fan = SerializerMethodField()
    is_hater = SerializerMethodField()
    total_likes = SerializerMethodField()
    total_dislikes = SerializerMethodField()
    rating = SerializerMethodField()
    image = Base64ImageField()
    is_favorited = BooleanField(read_only=True)

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
        user = self.context.get('request').user
        return likes_services.is_object_voted_by_user(
            obj,
            user,
            vote_type=Vote.Options.LIKE,
        )

    def get_is_hater(self, obj) -> bool:
        user = self.context.get('request').user
        return likes_services.is_object_voted_by_user(
            obj,
            user,
            vote_type=Vote.Options.DISLIKE,
        )

    def get_total_likes(self, obj) -> int:
        return obj.likes_count

    def get_total_dislikes(self, obj) -> int:
        return obj.dislikes_count

    def get_rating(self, obj) -> int:
        return obj.rating


class TagRootsSerializer(ModelSerializer):
    """Сериализатор для корневых тегов, модель Tag."""

    class Meta:
        model = Tag
        fields = [
            'pk',
            'name',
            'children',
        ]


class TagSerializer(TagRootsSerializer):
    """Сериализатор всех тогов, модель Tag."""

    class Meta(TagRootsSerializer.Meta):
        fields = TagRootsSerializer.Meta.fields + [
            'parent',
        ]
