from djoser.serializers import UserSerializer

from users.models import User


class CustomUserSerializer(UserSerializer):
    class Meta:
        model = User
        fields = ('uuid',
                  'email',
                  'first_name',
                  'last_name',
                  )


class CustomUserCreateSerializer(UserSerializer):
    class Meta:
        model = User
        fields = ('email',
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
