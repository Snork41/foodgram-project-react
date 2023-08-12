from django.contrib import admin

from users.models import User, Follow


@admin.register(User)
class UserAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'role',
        'email',
        'username',
        'first_name',
        'last_name'
    )
    empty_value_display = '-пусто-'
    list_filter = ('username', 'email',)


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'author',
    )
    empty_value_display = '-пусто-'
