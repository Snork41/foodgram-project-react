from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from api.filters import RecipeFilter
from api.pagination import RecipesPagination
from api.permissions import IsAuthorOrAdminOrReadOnly
from api.serializers import (FavoriteSerializer, IngredientSerializer,
                             RecipeGetSerializer, RecipeWriteSerializer,
                             ShoppingCartSerializer, TagSerializer)
from recipes.models import (Favorite, Ingredient, IngredientRecipe, Recipe,
                            ShoppingCart, Tag)


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('^name',)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    pagination_class = RecipesPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    permission_classes = (IsAuthorOrAdminOrReadOnly,)

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return RecipeGetSerializer
        return RecipeWriteSerializer

    @action(detail=True, methods=['post', 'delete'],
            permission_classes=[permissions.IsAuthenticated])
    def favorite(self, request, *args, **kwargs):
        user = self.request.user
        recipe = get_object_or_404(Recipe, id=self.kwargs.get('pk'))
        favorite_exists = Favorite.objects.filter(
            user=user, recipe=recipe).exists()
        if request.method == 'POST':
            if favorite_exists:
                return Response(
                    {"errors": "Этот рецепт уже добавлен в избранное!"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            serializer = FavoriteSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save(user=user, recipe=recipe)
                return Response(
                    serializer.data,
                    status=status.HTTP_201_CREATED
                )
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        if not favorite_exists:
            return Response(
                {"errors": "Рецепт не находится в избранном!"},
                status=status.HTTP_400_BAD_REQUEST
            )
        Favorite.objects.get(recipe=recipe, user=user).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['post', 'delete'],
            permission_classes=[permissions.IsAuthenticated])
    def shopping_cart(self, request, *args, **kwargs):
        user = self.request.user
        recipe = get_object_or_404(Recipe, id=self.kwargs.get('pk'))
        in_cart = ShoppingCart.objects.filter(
            user=user, recipe=recipe).exists()
        if request.method == 'POST':
            if in_cart:
                return Response(
                    {"errors": "Этот рецепт уже добавлен в список покупок!"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            serializer = ShoppingCartSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save(user=user, recipe=recipe)
                return Response(
                    serializer.data,
                    status=status.HTTP_201_CREATED
                )
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        if not in_cart:
            return Response(
                {"errors": "Рецепт не находится в списке покупок!"},
                status=status.HTTP_400_BAD_REQUEST
            )
        ShoppingCart.objects.get(recipe=recipe, user=user).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'],
            permission_classes=[permissions.IsAuthenticated])
    def download_shopping_cart(self, request, *args, **kwargs):
        ingredients = IngredientRecipe.objects.filter(
            recipe_id__shopping_cart__user=self.request.user).values(
            'ingredient__name', 'ingredient__measurement_unit').annotate(
            amount=Sum('amount')
        )
        shopping_list = ['>>>СПИСОК НЕОБХОДИМЫХ ИНГРЕДИЕНТОВ<<<\n']
        if not ingredients:
            shopping_list.append('УПС! Ваш список пуст :(')
        for index, ingredient in enumerate(ingredients, 1):
            raw = [
                str(index) + '.',
                ingredient['ingredient__name'].title() + ' -',
                str(ingredient['amount']),
                ingredient['ingredient__measurement_unit']
            ]
            shopping_list.append(' '.join(raw))
        response = HttpResponse(
            '\n'.join(shopping_list), content_type='text/plain'
        )
        response['Content-Disposition'] = (
            'attachment; filename="shopping_list.txt"'
        )
        return response
