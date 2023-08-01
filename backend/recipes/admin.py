from django.contrib import admin
from recipes.models import Ingredient, IngredientRecipe, Recipe, Tag

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
    ordering = ['name']
    empty_value_display = '-пусто-'


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'author',
    )
    list_filter = ('author', 'name', 'tags')
    empty_value_display = '-пусто-'
    inlines = (IngredientsInline,)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'color',
        'slug',
    )
    empty_value_display = '-пусто-'
