from django.contrib.auth import get_user_model
from djoser.serializers import UserSerializer as DjoserUserSerializer
from drf_extra_fields.fields import Base64ImageField
from rest_framework.serializers import BooleanField, ModelSerializer

from articles.models import Article

User = get_user_model()


class UserSerializer(DjoserUserSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'first_name',
            'last_name',
        )


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
    """Article serializer."""

    class Meta:
        model = Article
        fields = '__all__'  # TODO заменить на кортеж полей
        read_only_fields = ('created_at', 'updated_at', 'is_favorited')

    image = Base64ImageField()
    is_favorited = BooleanField()
