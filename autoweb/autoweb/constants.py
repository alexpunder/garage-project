# разрешенные символы для URL и username
USERNAME_PATTERN = r'^[a-zA-Z0-9_-]*$'
VIN_CODE_VALIDATOR = '^[0-9a-zA-Z]+$'

PRODUCTS_ON_INDEX_PAGE = 10  # количество товаров на домашней странице
PRODUCTS_ON_FILTER_PAGE = 9  # количество товаров на страницу с фильтром
PRODUCTS_ON_PAGE = 10  # количество товаров на странице списка товаров
PROMOTIONS_ON_PAGE = 3  # количество акций на странице
BRANDS_ON_INDEX_PAGE = 10

TITELES_DATA = {
    'filter_products_page': 'Страница товаров',
    'search_view': 'Результаты поиска',
    'categories_list_view': 'Список категорий',
    'subcategory_list_view': 'Список подкатегорий',
    'product_list_view': 'Товары категории',
    'product_detail_view': 'Страница товара',
    'brands_list_view': 'Список производителей',
    'brands_detail_view': 'Товары производителя',
    'promotions_detail_view': 'Страница акции',
    'PromotionsView': 'Список акций',
    'cart': 'Корзина товаров',
    'checkout': 'Оформление заказа'
}

# путь к условным 'фикстурам'
DB_DATA = {
    'category': 'shop/data/load_db_categories.csv',
    'subcategory': 'shop/data/load_db_subcategories.csv',
    'brand': 'shop/data/load_db_brands.csv',
    'product': 'shop/data/load_db_product.csv',
    'mark_auto': 'shop/data/load_db_mark_auto.csv'
}

# статусы заказов для клиентов и админов
ORDER_STATUS_CHOICES = [
    ('Без статуса', 'Без статуса'),
    ('Обработка заказа', 'Обработка заказа'),
    ('Ожидает самовывоза', 'Ожидает самовывоза'),
    ('Выдан', 'Выдан'),
    ('Отменен клиентом', 'Отменен клиентом'),
    ('Отменен магазином', 'Отменен магазином'),
    ('Возврат', 'Возврат')
]

# проверка статуса на возможность отмены заказа клиентом
ORDER_STATUS_CHECK = [
    'Без статуса',
    'Обработка заказа',
    'Ожидает самовывоза',
]

FILTERED_DATA = [
    'price_min', 'price_max', 'category', 'subcategory', 'brand'
]


NOTES = [
    ("Первый автомобиль в истории. В 1886 году Карл Бенц представил свой "
     "первый автомобиль, получивший название Benz Patent-Motorwagen. Это "
     "был трехколесный автомобиль с бензиновым двигателем мощностью 0.75 "
     "л.с. и максимальной скоростью около 16 км/ч. Это считается первым "
     "моторным автомобилем, созданным для массового производства."),
    ("Автомобиль, преодолевший наибольшее расстояние. Самый большой пробег "
     "у одного автомобиля за всю его жизнь был зафиксирован на Volvo P1800. "
     "Американец Ирв Гордон установил мировой рекорд, проехав на своем Volvo "
     "P1800 более 4,8 миллиона километров (почти 3 миллиона миль). Он "
     "катался на своем автомобиле более 50 лет, превратив его в легенду."),
    ("Самый быстрый серийный автомобиль. Bugatti Veyron 16.4 был признан "
     "самым быстрым серийным автомобилем в мире. Его максимальная скорость "
     "составляет около 431 км/ч. Этот элегантный суперкар имеет 1001 л.с. и "
     "может разгоняться до 100 км/ч всего за 2,5 секунды."),
    ("Инновации в безопасности: краш-тесты. Процедура краш-тестирования была "
     "разработана с целью тестирования и оценки безопасности автомобилей. "
     "Volvo была одной из первых компаний, которая начала применять "
     "краш-тесты для повышения безопасности своих автомобилей. С тех пор "
     "эта практика стала стандартной в индустрии, что способствовало "
     "существенному улучшению безопасности на дорогах."),
    ("Первый автомобиль с гибридным двигателем. Toyota Prius стала первым "
     "массовым производителем гибридных автомобилей. Она была представлена в "
     "1997 году в Японии и с тех пор стала символом экологически чистого "
     "движения в автомобильной промышленности. Сочетая бензиновый двигатель "
     "и электрический мотор, Prius снижает выбросы и экономит топливо, что "
     "делает её популярной среди экологически осознанных водителей.")
]