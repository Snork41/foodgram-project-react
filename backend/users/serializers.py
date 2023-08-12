from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers

from recipes.models import Recipe
from users.models import Follow, User


class UserCreateSerializer(UserCreateSerializer):

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


class UserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
        )

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        if user.is_authenticated:
            return user.follower.filter(author=obj).exists()
        return False


class RecipeInFollowSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time',
        )
        read_only_fields = ('__all__',)


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
    recipes = RecipeInFollowSerializer(
        many=True,
        read_only=True,
        source='author.recipes'
    )
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

    def get_is_subscribed(self, obj):
        if obj.user.is_authenticated:
            return Follow.objects.filter(
                user=obj.user, author=obj.author).exists()
        return False

    def get_recipes_count(self, obj):
        return Recipe.objects.filter(author=obj.author).count()
