from django.db import models
from django.core.validators import MinValueValidator

from users.models import User


class Tag(models.Model):
    """Тег."""

    BREAKFAST = 'Завтрак'
    DINNER = 'Обед'
    SUPPER = 'Ужин'
    TAG_NAME_CHOICES = [
        (BREAKFAST, 'Завтрак'),
        (DINNER, 'Обед'),
        (SUPPER, 'Ужин')
    ]
    name = models.CharField(
        choices=TAG_NAME_CHOICES,
        default=BREAKFAST,
        max_length=200,
        unique=True,
        verbose_name='Имя тега',
    )
    color = models.CharField(
        max_length=7,
        blank=True,
        verbose_name='Цветовой код',
    )
    slug = models.SlugField(
        max_length=200,
        unique=True,
        blank=True,
        verbose_name='Слаг',
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def save(self, *args, **kwargs):
        tags = {
            self.BREAKFAST: ('#f21624', 'breakfast'),
            self.DINNER: ('#28f216', 'dinner'),
            self.SUPPER: ('#b716f2', 'supper')
        }
        self.color, self.slug = tags[self.name]
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """Ингредиент."""

    name = models.CharField(
        max_length=200,
        verbose_name='Название ингредиента',
    )
    measurement_unit = models.CharField(
        max_length=200,
        verbose_name='Единица измерения',
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Рецепт."""

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор рецепта',
    )
    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name='Название рецепта',
    )
    image = models.ImageField(
        upload_to='recipes/images/',
        null=True,
        default=None,
    )
    text = models.TextField(
        verbose_name='Описание рецепта',
    )
    ingredients = models.ManyToManyField(
        'Ingredient',
        through='IngredientRecipe',
        verbose_name='Ингредиенты',
    )
    tags = models.ManyToManyField(
        'Tag',
        related_name='recipes',
        verbose_name='Теги',
    )
    cooking_time = models.PositiveIntegerField(
        verbose_name='Время приготовления (в минутах)',
        validators=[MinValueValidator(
            1, message='Минимальное время - 1 минута')]
    )

    pub_date = models.DateTimeField(
        verbose_name='Дата публикации рецепта',
        auto_now_add=True,
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class IngredientRecipe(models.Model):
    """Связная модель Ингредиент-Рецепт."""

    ingredient = models.ForeignKey(
        'Ingredient',
        on_delete=models.CASCADE,
    )
    recipe = models.ForeignKey(
        'Recipe',
        related_name='recipe_ingredients',
        on_delete=models.CASCADE,
    )
    amount = models.PositiveIntegerField(
        verbose_name='Количество',
        validators=[MinValueValidator(
            1, message='Минимальное количество - 1')]
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='unique_ingredient_in_recipe'),
        ]

    def __str__(self):
        return f'{self.ingredient} - {self.recipe}'


class Favorite(models.Model):
    """Избранное."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorite',
        verbose_name='Пользователь',
    )

    recipe = models.ForeignKey(
        'Recipe',
        on_delete=models.CASCADE,
        related_name='favorite',
        verbose_name='Рецепт в спике избранных',
    )

    class Meta:
        verbose_name = 'Рецепт в списке избранных'
        verbose_name_plural = 'Рецепты в списке избранных'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_favorite'),
        ]

    def __str__(self):
        return self.recipe.name


class ShoppingCart(models.Model):
    """Список покупок."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='Пользователь',
    )

    recipe = models.ForeignKey(
        'Recipe',
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='Рецепт в корзине',
    )

    class Meta:
        verbose_name = 'Рецепт в корзине'
        verbose_name_plural = 'Рецепты в корзине'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_cart'),
        ]

    def __str__(self):
        return self.recipe.name
