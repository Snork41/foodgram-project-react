from rest_framework import serializers

from recipes.models import Follow
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'password',
        )


class FollowSerializer(serializers.ModelSerializer):
    email = serializers.ReadOnlyField(
        source='author.email',
        read_only=True
    )
    id = serializers.PrimaryKeyRelatedField(
        source='author.id',
        read_only=True
    )
    username = serializers.ReadOnlyField(
        source='author.username',
        read_only=True
    )
    first_name = serializers.ReadOnlyField(
        source='author.first_name',
        read_only=True
    )
    last_name = serializers.ReadOnlyField(
        source='author.last_name',
        read_only=True
    )
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = Follow
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count',
        )
