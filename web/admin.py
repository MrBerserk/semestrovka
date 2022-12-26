from import_export import resources
from import_export.admin import ImportExportModelAdmin

from django.contrib import admin

from .models import Favourite, Game, Basket, Comment, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    list_per_page = 5
    ordering = ['name']


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


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['game', 'user', 'text']
    list_per_page = 5
    ordering = ['user']


class GameResource(resources.ModelResource):
    class Meta:
        model = Game
        fields = ('title', 'slug', 'description', 'image', 'price')
        export_order = ('title', 'slug', 'description', 'image', 'price')


class GameAdmin(ImportExportModelAdmin):
    resource_classes = [GameResource]
    ordering = ['created_at']
    list_select_related = ['user']
    list_display = ['title', 'slug', 'description', 'price', 'image',
                    'user']
    readonly_fields = ['id']
    fields = [('title', 'slug'), 'description', 'price', 'image',
              'user', 'category']
    list_filter = ['created_at']
    filter_horizontal = ['category']
    prepopulated_fields = {'slug': ('title',)}
    resource_classes = [GameResource]


admin.site.register(Game, GameAdmin)
