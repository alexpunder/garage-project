from django.urls import path

from .views import (HomepageView, PromotionsView, brands_detail_view,
                    brands_list_view, categories_list_view,
                    filter_products_page, product_detail_view,
                    product_list_view, promotions_detail_view, search_view,
                    subcategory_list_view)

app_name = 'shop'

urlpatterns = [
    path(
        '',
        HomepageView.as_view(),
        name='homepage'
    ),
    path(
        'categories/',
        categories_list_view,
        name='categories_list'
    ),
    path(
        '<slug:category_slug>/subcategories/',
        subcategory_list_view,
        name='subcategory_list'
    ),
    path(
        ('<slug:category_slug>/<slug:subcategory_slug>/products/'),
        product_list_view,
        name='product_list'
    ),
    path(
        '<slug:category_slug>/<slug:subcategory_slug>/<int:pk>/',
        product_detail_view,
        name='product_detail'
    ),
    path(
        'brands/',
        brands_list_view,
        name='brands_list'
    ),
    path(
        'brands/<slug:slug_brand>/',
        brands_detail_view,
        name='brand_detail'
    ),
    path(
        'search/',
        search_view,
        name='search',
    ),
    path(
        'promotions/',
        PromotionsView.as_view(),
        name='promotions',
    ),
    path(
        'promotions/<int:pk>/',
        promotions_detail_view,
        name='promotion_detail',
    ),
    path(
        'all-products/',
        filter_products_page,
        name='all_products'
    )
]
