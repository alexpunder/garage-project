from django.contrib import admin

from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    fields = (
        'product', 'product_article', 'product_brand', 'quantity'
    )
    readonly_fields = (
        'product', 'product_article', 'product_brand', 'quantity'
    )

    def product_article(self, obj):
        return obj.product.article
    product_article.short_description = 'Артикул'

    def product_brand(self, obj):
        return obj.product.brand
    product_brand.short_description = 'Бренд'


class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]
    list_display = ('id', 'user', 'created_at')
    list_display_links = ('id', 'user')
    search_fields = ('id', 'user__username')
    list_per_page = 25


admin.site.register(Order, OrderAdmin)
