from django.shortcuts import get_object_or_404
from recipes.models import Favorite, Ingredient, Recipe, Tag
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .pagination import RecipesPagination
from .serializers import (FavoriteSerializer, IngredientSerializer,
                          RecipeGetSerializer, RecipeWriteSerializer,
                          TagSerializer)


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    pagination_class = RecipesPagination

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
            author=user, recipe=recipe).exists()
        if request.method == 'POST':
            if favorite_exists:
                return Response(
                    {"errors": "Этот рецепт уже добавлен в избранное!"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            serializer = FavoriteSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save(author=user, recipe=recipe)
                return Response(
                    serializer.data,
                    status=status.HTTP_201_CREATED
                )
            return
        if not favorite_exists:
            return Response(
                {"errors": "Рецепт не находится в избранном!"},
                status=status.HTTP_400_BAD_REQUEST
            )
        Favorite.objects.get(recipe=recipe).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
