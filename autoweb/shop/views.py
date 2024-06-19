from django.contrib import messages
from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView

from autoweb.constants import (BRANDS_ON_INDEX_PAGE, PRODUCTS_ON_FILTER_PAGE,
                               PRODUCTS_ON_INDEX_PAGE, PRODUCTS_ON_PAGE,
                               PROMOTIONS_ON_PAGE, TITELES_DATA)
from shop.models import Brand, Category, Product, Promotions

from .filters import ProductFilter, SearchFilter
from .services import ShopServices
from .utils import (convert_specification_and_crosslist_to_valid_data,
                    get_filters_count, paginate_items)
from .validators import check_filtered_products


def filter_products_page(request):
    """
    Представление для отображения выбранных в блоке фильтров товаров.
    """
    template = 'product/filter_products_page.html'
    product_filter = ShopServices.get_filtered_products(
        ProductFilter, request.GET
    )
    filters_count = get_filters_count(product_filter)

    context = {
        'filter': product_filter,
        'title': TITELES_DATA['filter_products_page'],
        'filters_count': filters_count
    }

    if product_filter.qs:
        page_obj = paginate_items(
            request, product_filter.qs, PRODUCTS_ON_FILTER_PAGE
        )
        context['page_obj'] = page_obj
        context['products_count'] = product_filter.qs.count()
        return render(request, template, context)
    else:
        messages.info(
            request, 'К сожалению, ничего не найдено...'
        )
        return render(request, template, context)


def search_view(request):
    """
    Представление для отображения найденных товаров по данным, введенным
    в поле поиска в header страницы сайта.
    """
    template = 'util_pages/search.html'
    product_search = ShopServices.get_filtered_products(
        SearchFilter, request.GET
    )

    context = {
        'filter': product_search,
        'title': TITELES_DATA['search_view']
    }

    if check_filtered_products(request, product_search):
        page_obj = paginate_items(
            request, product_search.qs, PRODUCTS_ON_PAGE
        )
        context['page_obj'] = page_obj
        return render(request, template, context)

    return render(request, template, context)


class HomepageView(ListView):
    """
    Представление для отображения главной страницы сайта.
    """
    model = Product
    template_name = 'util_pages/index.html'
    context_object_name = 'product_list'
    queryset = Product.objects.select_related(
        'category',
        'subcategory',
        'brand',
    ).filter(
        is_published=True,
        quantity__gt=0,
        price__gt=0,
        category__is_published=True,
        brand__title='MOTUL',
        # output_order__gte=100,
    ).order_by(
        'subcategory__title',
        'price'
    )[:PRODUCTS_ON_INDEX_PAGE]

    def get_queryset(self):
        brands = Brand.objects.filter(
            is_published=True,
        ).order_by(
            'title'
        )[:BRANDS_ON_INDEX_PAGE]
        self.extra_context = {'brands': brands}
        return super().get_queryset()


class PromotionsView(ListView):
    """
    Представление для отображения всех рекламных постов на странице "Акции".
    """
    model = Promotions
    template_name = 'promotions/promotions_list.html'
    paginate_by = PROMOTIONS_ON_PAGE
    queryset = Promotions.objects.filter(
        is_published=True,
    ).order_by(
        '-id'
    )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = TITELES_DATA['PromotionsView']
        return context


def categories_list_view(request):
    """
    Представление для отображения всех категорий товаров.
    """
    template = 'product/categories_list.html'
    categories_list = Category.objects.order_by('title')
    context = {
        'categories_list': categories_list,
        'title': TITELES_DATA['categories_list_view']
    }
    return render(request, template, context)


def subcategory_list_view(request, category_slug):
    """
    Представление для отображения всех подкатегорий выбранной категории
    товаров.
    """
    category = get_object_or_404(Category, slug=category_slug)
    template = 'product/subcategories_list.html'
    subcategories = category.subcategories.order_by('title')
    context = {
        'category': category,
        'subcategories': subcategories,
        'title': TITELES_DATA['subcategory_list_view']
    }
    return render(request, template, context)


def product_list_view(request, category_slug, subcategory_slug):
    """
    Представление для отображения всех товаров выбранной подкатегории
    из категории.
    """
    products = ShopServices.get_products_by_category_and_subcategory(
        category_slug, subcategory_slug
    )
    page_obj = paginate_items(
        request, products, PRODUCTS_ON_PAGE
    )
    context = {
        'page_obj': page_obj,
        'category_slug': category_slug,
        'title': TITELES_DATA['product_list_view']
    }
    return render(request, 'product/product_list.html', context)


def brands_list_view(request):
    """
    Представление для отображения всех производителей товаров.
    """
    template = 'brands/brands_list.html'
    brands_list = Brand.objects.order_by('title')
    context = {
        'brands_list': brands_list,
        'title': TITELES_DATA['brands_list_view']
    }
    return render(request, template, context)


def brands_detail_view(request, slug_brand):
    """
    Представление для отображения списка товаров выбранного производителя.
    """
    template_name = 'brands/brands_detail.html'
    brands_detail = Product.objects.filter(
        is_published=True,
        quantity__gt=0,
        price__gt=0,
        brand__slug_brand=slug_brand
    ).select_related(
        'category',
        'subcategory',
        'brand',
    ).order_by(
        'brand__title',
        'price'
    )
    page_obj = paginate_items(
        request, brands_detail, PRODUCTS_ON_PAGE
    )
    context = {
        'page_obj': page_obj,
        'title': TITELES_DATA['brands_detail_view']
    }
    return render(request, template_name, context)


def promotions_detail_view(request, pk):
    """
    Представление для детального отображения поста выбранной акции.
    """
    template_name = 'promotions/promotion.html'
    promotion = get_object_or_404(Promotions, pk=pk)
    context = {
        'promotion': promotion,
    }
    return render(request, template_name, context)


def product_detail_view(request, pk, category_slug, subcategory_slug):
    """
    Представление для детального отображения выбранного товара либо на
    странице со списком товаров из 'product_list_view', либо с главной
    страницы сайта, либо со страницы товаров выбранного производителя.
    """
    template_name = 'product/product_detail.html'
    product = ShopServices.get_single_product_by_category_and_subcategory(
        pk, category_slug, subcategory_slug
    )
    images = product.images.all()

    context = {
        'product': product,
        'images': images,
        'title': TITELES_DATA['product_detail_view'],
        'category_slug': category_slug,
        'subcategory_slug': subcategory_slug,
    }

    if product.specification and product.cross_list:
        convert_specification_and_crosslist_to_valid_data(
            context, product.specification, product.cross_list
        )
        return render(request, template_name, context)

    return render(request, template_name, context)
