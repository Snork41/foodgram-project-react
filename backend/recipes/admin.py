from django.contrib import admin

from recipes.models import Ingredient, Recipe, Tag


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'measurement_unit',
    )
    fields = (
        'name',
        'measurement_unit',
    )
    empty_value_display = '-пусто-'


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'image',
        'text',
        'cooking_time',
        'author',
    )
    fields = (
        'name',
        'image',
        'text',
        'cooking_time',
        'author',
    )
    empty_value_display = '-пусто-'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'color',
        'slug',
    )
    fields = (
        'name',
        'color',
        'slug',
    )
    empty_value_display = '-пусто-'


admin.site.site_header = '"FOODGRAM" | Администрирование'
