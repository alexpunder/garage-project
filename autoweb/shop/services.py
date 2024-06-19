from django.shortcuts import get_object_or_404

from .models import Category, Product, Subcategory


class ShopServices:

    @staticmethod
    def get_products_by_category_and_subcategory(
        category_slug, subcategory_slug
    ):
        category = get_object_or_404(
            Category, slug=category_slug
        )
        subcategory = get_object_or_404(
            Subcategory, slug=subcategory_slug, category=category
        )
        products = Product.objects.filter(
            category=category,
            subcategory=subcategory,
            is_published=True,
            quantity__gt=0,
            price__gt=0
        ).order_by(
            'title',
        )
        return products

    @staticmethod
    def get_single_product_by_category_and_subcategory(
        pk, category_slug, subcategory_slug
    ):
        category = get_object_or_404(
            Category, slug=category_slug
        )
        subcategory = get_object_or_404(
            Subcategory, slug=subcategory_slug, category=category
        )
        product = get_object_or_404(
            Product, pk=pk, category=category, subcategory=subcategory
        )
        return product

    @staticmethod
    def get_filtered_products(filter_class, request_data):
        filtered_products = filter_class(
            request_data, Product.objects.filter(
                is_published=True,
                quantity__gt=0,
                price__gt=0
            ).select_related(
                'category',
                'subcategory',
                'brand',
            ).order_by(
                'brand__title',
                'price'
            )
        )
        return filtered_products
