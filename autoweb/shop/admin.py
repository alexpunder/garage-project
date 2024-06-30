from django.contrib import admin
from django.utils.text import Truncator

from .models import (Brand, Category, CSVLoaderDB, Product, ProductImage,
                     Promotions, Subcategory)

admin.site.empty_value_display = 'Не задано'


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]
    list_display = (
        'id',
        'short_title',
        'brand',
        'article',
        'price',
        'output_order',
    )
    list_select_related = (
        'category',
        'subcategory',
        'brand',
    )
    list_editable = (
        'price',
        'output_order',
    )
    search_fields = ('id', 'article',)
    list_filter = ('category', 'subcategory', 'brand',)
    list_display_links = ('short_title',)
    list_per_page = 25

    def short_title(self, obj):
        return Truncator(obj.title).chars(20)

    short_title.short_description = 'Название'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'title', 'slug'
    )
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'title', 'slug'
    )
    list_select_related = (
        'category',
    )
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'is_on_main',
    )
    list_editable = (
        'is_on_main',
    )
    list_filter = (
        'is_on_main',
    )
    prepopulated_fields = {'slug_brand': ('title',)}


@admin.register(Promotions)
class PromotionsAdmin(admin.ModelAdmin):
    list_display = (
        'short_title',
        'short_description',
        'image',
        'pub_date',
    )

    def short_title(self, obj):
        return Truncator(obj.title).chars(20)

    short_title.short_description = 'Название'

    def short_description(self, obj):
        return Truncator(obj.title).chars(20)

    short_description.short_description = 'Содержание'


admin.site.register(ProductImage)


@admin.register(CSVLoaderDB)
class CSVLoaderDBAdmin(admin.ModelAdmin):
    pass
