import base64

from django.db import transaction
from django.core.files.base import ContentFile
from recipes.models import (Favorite, Ingredient, IngredientRecipe,
                            Recipe, ShoppingCart, Tag)
from rest_framework import serializers
from users.serializers import UserSerializer


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            imgformat, imgstr = data.split(';base64,')
            extension = imgformat.split('/')[-1]
            data = ContentFile(
                base64.b64decode(imgstr), name='image.' + extension
            )
        return super().to_internal_value(data)


class ShoppingCartSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        source='recipe.id',
        read_only=True
    )
    name = serializers.ReadOnlyField(
        source='recipe.name',
        read_only=True
    )
    image = serializers.ImageField(
        source='recipe.image',
        read_only=True
    )
    cooking_time = serializers.IntegerField(
        source='recipe.cooking_time',
        read_only=True)

    class Meta:
        model = ShoppingCart
        fields = (
            'id',
            'name',
            'image',
            'cooking_time',
        )


class FavoriteSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        source='recipe.id',
        read_only=True
    )
    name = serializers.ReadOnlyField(
        source='recipe.name',
        read_only=True
    )
    image = serializers.ImageField(
        source='recipe.image',
        read_only=True
    )
    cooking_time = serializers.IntegerField(
        source='recipe.cooking_time',
        read_only=True)

    class Meta:
        model = Favorite
        fields = (
            'id',
            'name',
            'image',
            'cooking_time',
        )


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = (
            'id',
            'name',
            'measurement_unit',
        )
        read_only_fields = ('__all__',)


class IngredientRecipeSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(
        source='ingredient.id'
    )
    name = serializers.ReadOnlyField(
        source='ingredient.name'
    )
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )
    amount = serializers.ReadOnlyField()

    class Meta:
        model = IngredientRecipe
        fields = (
            'id',
            'name',
            'measurement_unit',
            'amount',
        )


class IngredientForRecipeSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all(),
    )
    amount = serializers.IntegerField()

    class Meta:
        model = IngredientRecipe
        fields = (
            'id',
            'amount',
        )


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = (
            'id',
            'name',
            'color',
            'slug',
        )
        read_only_fields = ('__all__',)


class RecipeGetSerializer(serializers.ModelSerializer):
    author = UserSerializer()
    tags = TagSerializer(many=True, read_only=True)
    ingredients = IngredientRecipeSerializer(
        many=True,
        source='recipe_ingredients',
        read_only=True
    )
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time',
        )

    def get_is_favorited(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return Favorite.objects.filter(
            user=user, recipe=obj).exists()

    def get_is_in_shopping_cart(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return ShoppingCart.objects.filter(
            user=user, recipe=obj).exists()


class RecipeWriteSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True
    )
    ingredients = IngredientForRecipeSerializer(
        many=True,
        write_only=True
    )
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'name',
            'image',
            'text',
            'cooking_time',
        )

    @transaction.atomic
    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        for ingredient in ingredients:
            IngredientRecipe.objects.create(
                recipe=recipe,
                ingredient=ingredient['id'],
                amount=ingredient['amount']
                )
        recipe.tags.set(tags)
        return recipe

    def update(self, instance, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        Recipe.objects.filter(name=instance.name).update(**validated_data)
        recipe = Recipe.objects.get(name=instance.name)
        instance.ingredients.clear()
        instance.tags.clear()
        for ingredient in ingredients:
            IngredientRecipe.objects.update_or_create(
                recipe=recipe,
                ingredient=ingredient['id'],
                amount=ingredient['amount']
                )
        recipe.tags.set(tags)
        return recipe

    def to_representation(self, instance):
        recipe = super().to_representation(instance)
        recipe['ingredients'] = IngredientRecipeSerializer(
            instance.recipe_ingredients.all(),
            many=True).data
        recipe['tags'] = TagSerializer(instance.tags.all(), many=True).data
        recipe['author'] = UserSerializer(instance.author).data
        return recipe

    def validate_tags(self, tags):
        if not tags:
            raise serializers.ValidationError('Выберите тег!')
        if len(tags) > len(set(tags)):
            raise serializers.ValidationError('Теги нельзя повторять!')
        return tags

    def validate_ingredients(self, ingredients):
        list_ingredients = []
        if not ingredients:
            raise serializers.ValidationError('Выберите ингредиенты!')
        for ingredient in ingredients:
            if not ingredient['amount']:
                raise serializers.ValidationError(
                    'Количество ингредиента должно быть больше 0!'
                )
            if ingredient['id'] in list_ingredients:
                raise serializers.ValidationError(
                    'Ингредиенты не должны повторяться!'
                )
            list_ingredients.append(ingredient['id'])
        return ingredients
