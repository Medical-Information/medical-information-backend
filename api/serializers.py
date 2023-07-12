from django.contrib.auth import get_user_model
from djoser import serializers
from drf_extra_fields.fields import Base64ImageField
from rest_framework.serializers import ModelSerializer, SerializerMethodField

from articles.models import Article
from likes import services as likes_services
from likes.models import LikeDislike

User = get_user_model()


class UserSerializer(serializers.UserSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'first_name',
            'last_name',
        )


class UserCreateSerializer(serializers.UserSerializer):
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
    """Article serializer."""

    class Meta:
        model = Article
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at',
                            'total_likes', 'total_dislikes',
                            )

    is_fan = SerializerMethodField()
    is_hater = SerializerMethodField()
    total_likes = SerializerMethodField()
    total_dislikes = SerializerMethodField()
    rating = SerializerMethodField()
    image = Base64ImageField()

    def get_is_fan(self, obj) -> bool:
        user = self.context.get('request').user
        return likes_services.is_group(obj, user, vote_type=LikeDislike.LIKE)

    def get_is_hater(self, obj) -> bool:
        user = self.context.get('request').user
        return likes_services.is_group(obj, user, vote_type=LikeDislike.DISLIKE)

    def get_total_likes(self, obj):
        return obj.likes_count

    def get_total_dislikes(self, obj):
        return obj.dislikes_count

    def get_rating(self, obj):
        return obj.rating
