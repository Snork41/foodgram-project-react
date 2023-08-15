from django.db.models import Sum
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, viewsets
from rest_framework.decorators import action

from api.filters import IngredientFilter, RecipeFilter
from api.pagination import RecipesPagination
from api.permissions import IsAuthorOrAdminOrReadOnly
from api.serializers import (FavoriteSerializer, IngredientSerializer,
                             RecipeGetSerializer, RecipeWriteSerializer,
                             ShoppingCartSerializer, TagSerializer)
from api.mixins import AddOrDelCartFavoriteMixin
from recipes.models import (Favorite, Ingredient, IngredientRecipe, Recipe,
                            ShoppingCart, Tag)


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (IngredientFilter,)
    search_fields = ('^name',)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class RecipeViewSet(viewsets.ModelViewSet, AddOrDelCartFavoriteMixin):
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
        return self.action_for_cart_or_favorite(
            request,
            Favorite,
            FavoriteSerializer
        )

    @action(detail=True, methods=['post', 'delete'],
            permission_classes=[permissions.IsAuthenticated])
    def shopping_cart(self, request, *args, **kwargs):
        return self.action_for_cart_or_favorite(
            request,
            ShoppingCart,
            ShoppingCartSerializer
        )

    @action(detail=False, methods=['get'],
            permission_classes=[permissions.IsAuthenticated])
    def download_shopping_cart(self, request, *args, **kwargs):
        ingredients = IngredientRecipe.objects.filter(
            recipe_id__shopping_cart__user=self.request.user).values(
            'ingredient__name', 'ingredient__measurement_unit').annotate(
            amount_ingredients=Sum('amount')
        )
        shopping_list = ['>>>СПИСОК НЕОБХОДИМЫХ ИНГРЕДИЕНТОВ<<<\n']
        if not ingredients:
            shopping_list.append('УПС! Ваш список пуст :(')
        for index, ingredient in enumerate(ingredients, 1):
            raw = [
                str(index) + '.',
                ingredient['ingredient__name'].title() + ' -',
                str(ingredient['amount_ingredients']),
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
