from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response

from recipes.models import Recipe


class AddOrDelCartFavoriteMixin:

    def action_for_cart_or_favorite(
            self,
            request,
            model,
            serializer,
            *args,
            **kwargs):
        name_model = model.__doc__
        user = self.request.user
        recipe = get_object_or_404(Recipe, id=self.kwargs.get('pk'))
        relation_exist = model.objects.filter(
            user=user, recipe=recipe).exists()
        if request.method == 'POST':
            if relation_exist:
                return Response(
                    {"errors": "Этот рецепт уже есть в {}".format(name_model)},
                    status=status.HTTP_400_BAD_REQUEST
                )
            serializer = serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(user=user, recipe=recipe)
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED)
        if not relation_exist:
            return Response(
                {"errors": "Рецепт не находится в {}'".format(name_model)},
                status=status.HTTP_400_BAD_REQUEST
            )
        model.objects.get(recipe=recipe, user=user).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
