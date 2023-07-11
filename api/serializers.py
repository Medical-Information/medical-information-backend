from django.contrib.auth import get_user_model
from djoser import serializers
from drf_extra_fields.fields import Base64ImageField
from rest_framework.serializers import ModelSerializer, SerializerMethodField
from likes import services as likes_services

from articles.models import Article

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
        read_only_fields = ('created_at', 'updated_at', 'total_likes')

    is_fan = SerializerMethodField()
    total_likes = SerializerMethodField()
    image = Base64ImageField()

    def get_is_fan(self, obj) -> bool:
        user = self.context.get('request').user
        return likes_services.is_fan(obj, user)

    def get_total_likes(self, obj):
        return obj.likes_count


class FanSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            'email',
            'first_name',
            'last_name',
        )

    full_name = SerializerMethodField()

    def get_full_name(self, obj):
        return obj.get_full_name()
