from django.contrib import admin

from .models import Favourite, Game, Basket


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'description', 'price', 'image',
                    'user']
    list_per_page = 6
    fields = [('title', 'slug'), 'description', 'price', 'image',
              'user']
    search_fields = ['title']
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Favourite)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ['user', 'game']
    list_per_page = 5
    ordering = ['game']


class BasketAdminInLine(admin.TabularInline):
    model = Basket
    fields = ['game', 'created_timestamp']
    readonly_fields = ['created_timestamp', 'game']
    extra = 0
