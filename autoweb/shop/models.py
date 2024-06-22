from csv import DictReader
from io import TextIOWrapper

from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils.text import slugify
from PIL import Image

from .validators import validate_csv_file

User = get_user_model()


class BaseModel(models.Model):
    title = models.CharField(
        'Название',
        max_length=255,
    )
    is_published = models.BooleanField(
        'Опубликовано',
        default=True,
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.title


class Product(BaseModel):
    description = models.TextField(
        'Описание',
        default='',
        blank=True
    )
    specification = models.TextField(
        'Спецификация',
        default='',
        blank=True
    )
    cross_list = models.TextField(
        'Кросс-лист',
        default='',
        blank=True
    )
    article = models.CharField(
        'Артикул',
        max_length=255
    )
    quantity = models.PositiveSmallIntegerField(
        'Количество товара на складе',
        default=0,
    )
    category = models.ForeignKey(
        'Category',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Категория',
    )
    subcategory = models.ForeignKey(
        'Subcategory',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Подкатегория',
    )
    brand = models.ForeignKey(
        'Brand',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Производитель',
    )
    price = models.DecimalField(
        'Цена',
        max_digits=7,
        decimal_places=2,
    )
    output_order = models.PositiveSmallIntegerField(
        'Приоритет',
        default=0,
    )

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def get_absolute_url(self):
        return reverse(
            'shop:product_detail', kwargs={
                'category_slug': self.category.slug,
                'subcategory_slug': self.subcategory.slug,
                'pk': self.pk
            }
        )


class ProductImage(models.Model):
    product = models.ForeignKey(
        'Product',
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name='Товар',
    )
    image = models.ImageField(
        'Изображение',
        upload_to='product_images',
    )

    class Meta:
        verbose_name = 'Изображение продукта'
        verbose_name_plural = 'Изображения продукта'

    def __str__(self):
        return f'Изображение для: {self.product.title}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)
        img.thumbnail((700, 700))
        img.save(self.image.path)


class Category(BaseModel):
    slug = models.SlugField(
        'Идентификатор',
        unique=True,
    )
    image = models.ImageField(
        'Изображение',
        upload_to='category_images',
        null=True,
        blank=True,
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

        if self.image:
            img = Image.open(self.image.path)
            img.thumbnail((700, 700))
            img.save(self.image.path)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def get_absolute_url(self):
        return reverse(
            'shop:subcategory_list',
            kwargs={'category_slug': self.slug}
        )


class Subcategory(BaseModel):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='subcategories',
        verbose_name='Категория',
    )
    slug = models.SlugField(
        'Идентификатор',
        unique=True,
    )
    image = models.ImageField(
        'Изображение',
        upload_to='subcategory_images',
        null=True,
        blank=True,
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

        if self.image:
            img = Image.open(self.image.path)
            img.thumbnail((700, 700))
            img.save(self.image.path)

    class Meta:
        verbose_name = 'Подкатегория'
        verbose_name_plural = 'Подкатегории'

    def get_absolute_url(self):
        return reverse(
            'shop:product_list',
            kwargs={
                'category_slug': self.category.slug,
                'subcategory_slug': self.slug,
            }
        )


class Brand(BaseModel):
    is_on_main = models.BooleanField(
        'Выводить ли на главной?',
        default=False,
    )
    description = models.TextField(
        verbose_name='Описание',
        blank=True
    )
    slug_brand = models.SlugField(
        'Идентификатор бренда',
        unique=True,
    )
    producing_country = models.CharField(
        'Страна производства',
        max_length=255,
        null=True,
        blank=True
    )
    image = models.ImageField(
        'Изображение',
        upload_to='brands_images',
        null=True,
        blank=True,
    )

    def save(self, *args, **kwargs):
        if not self.slug_brand:
            self.slug_brand = slugify(self.title)
        super().save(*args, **kwargs)

        if self.image:
            img = Image.open(self.image.path)
            img.thumbnail((700, 700))
            img.save(self.image.path)

    class Meta:
        verbose_name = 'Производитель'
        verbose_name_plural = 'Производители'

    def get_absolute_url(self):
        return reverse(
            'shop:brand_detail',
            kwargs={'slug_brand': self.slug_brand}
        )


class Promotions(BaseModel):
    description = models.TextField(
        verbose_name='Описание'
    )
    image = models.ImageField(
        'Изображение',
        upload_to='promotions_images',
        null=True,
        blank=True,
    )
    pub_date = models.DateTimeField(
        'Дата создания',
        auto_now=True,
    )

    class Meta:
        verbose_name = 'акция'
        verbose_name_plural = 'Акции'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.image:
            img = Image.open(self.image.path)
            img.thumbnail((730, 490))
            img.save(self.image.path)

    def get_absolute_url(self):
        return reverse(
            'shop:promotion_detail',
            kwargs={'pk': self.pk}
        )


class CSVLoaderDB(models.Model):
    file = models.FileField(
        upload_to='csv_files/',
        validators=[validate_csv_file]
    )

    class Meta:
        verbose_name = 'Загрузка прайсов'
        verbose_name_plural = 'Загрузка прайсов'

    def __str__(self):
        return 'Файл обновления цены/количества'


@receiver(post_save, sender=CSVLoaderDB)
def process_csv_file_after_save(sender, instance, **kwargs):
    handle_uploaded_file(instance.file)


def handle_uploaded_file(csv_loader_instance):
    if csv_loader_instance.file:
        with csv_loader_instance.file.open(mode='r') as file:
            text_wrapper = TextIOWrapper(file, encoding='utf-8-sig')
            reader = DictReader(text_wrapper, delimiter=';')
            for row in reader:

                if not Product.objects.filter(id=row['id']).exists():
                    continue

                if row.get('quantity'):
                    quantity_int = int((row['quantity'].split(','))[0])
                    row['quantity'] = quantity_int
                if row.get('price'):
                    price_str = str(row['price']).split(',')
                    price = int(price_str[0].replace(' ', ''))
                    row['price'] = price

                product = Product.objects.get(id=row['id'])
                product.quantity = row['quantity']
                product.price = row['price']
                product.save()
