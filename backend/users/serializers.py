from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers

from recipes.models import Recipe
from users.models import Follow, User
from users.mixins import IsSubscribedMixin


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


class UserSerializer(UserSerializer, IsSubscribedMixin):
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
        author = obj
        return self.is_subscribed(author)


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


class FollowSerializer(serializers.ModelSerializer, IsSubscribedMixin):
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

    def get_is_subscribed(self, obj):
        author = obj.author
        return self.is_subscribed(author)

    def get_recipes(self, obj):
        request = self.context.get('request')
        limit = request.GET.get('recipes_limit')
        recipes = Recipe.objects.filter(author=obj.author)
        if limit and limit.isdigit():
            recipes = recipes[:int(limit)]
        return RecipeInFollowSerializer(recipes, many=True).data

    def get_recipes_count(self, obj):
        return Recipe.objects.filter(author=obj.author).count()
