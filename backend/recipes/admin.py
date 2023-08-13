from django.contrib import admin

from recipes.models import (Favorite, Ingredient, IngredientRecipe,
                            Recipe, ShoppingCart, Tag)

admin.site.site_header = '"FOODGRAM" | Администрирование'


class IngredientsInline(admin.TabularInline):
    model = IngredientRecipe
    extra = 5
    verbose_name = 'Ингредиент'
    verbose_name_plural = 'Ингредиенты'


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'measurement_unit',
    )
    ordering = ['id']
    empty_value_display = '-пусто-'
    list_filter = ('name',)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'author',
        'amount_favorites',
    )
    list_filter = ('author', 'name', 'tags')
    filter_horizontal = ('tags',)
    empty_value_display = '-пусто-'
    inlines = (IngredientsInline,)

    def amount_favorites(self, obj):
        return obj.favorite.count()
    amount_favorites.short_description = 'Количество добавлений в избранное'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'color',
        'slug',
    )
    fields = ('name',)
    empty_value_display = '-пусто-'


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'recipe',
    )
    empty_value_display = '-пусто-'


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'recipe',
    )
    empty_value_display = '-пусто-'
